#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module allow to make calculation for the shear force
"""
import sys
import math

import mpmath

from shear.vrdc import vrdc
from shear.theta import theta

# sys.path.append(sys.path[0]+'/../Office_lib')
# import TWord

class Shear:
    """
        Class to do all calculation about the Shear
    """

    def __init__(self, internal_force, cross_section, mat_steel, mat_concrete, **kwargs):
        """
            Constructor

            :@param internal_force: Med, Ved, Ned; depend what we want to caculate
            :@param cross_section: section property
            :@param mat_steel: material property of steel
            :@param mat_concrete: material property of concrete
            :@param **kwarg: parameter to make the class standalone
            :@type internal_force: dict or float or int
            :@type cross_section: section object
            :@type mat_steel: material object
            :@type mat_concrete: materia object
        """
        if isinstance(internal_force, dict):
            self.__medu = internal_force["MED"]
            self.__vedu = internal_force["VED"]
            self.__nedu = internal_force["NED"]

        elif isinstance(internal_force, (float, int)):
            self.__medu = 0
            self.__vedu = internal_force
            self.__nedu = 0

        self.__vedu_red = self.__vedu

        self.__section = cross_section
        self.__mat_steel = mat_steel
        self.__mat_concrete = mat_concrete

        self.__b = self.__section.b
        self.__d = self.__section.d
        self.__z = self.__d * 0.9

        self.__alpha = self.__section.ALPHA_SHEAR
        self.__cot_alpha = 1 / (math.tan(math.radians(self.__alpha)))

        # Variable that will be used
        self.asw_s = None
        self.alpha_cw = None
        self.__section_kind = None
        self.theta = None
        self.__cot_theta = None

        # Vrd,c
        self.vrdc = None
        self.vrdc_1 = None
        self.vrdc_2 = None
        self.vmin = None

        # Vrd max
        self.nu = 0.6 * (1 - self.__mat_concrete.fck / 250)
        self.vrdmax = None

        # sigma_rdc
        self.sigma_rdc = None

        # As support
        self.fe = None
        self.as_support = None

        # Roh_min
        self.roh_min = None

        # Asmin
        self.asw_min = None

        # st_max
        self.st_max = None

        # sl_max
        self.sl_max = None

    def make_calculation(self, kind="BEAM"):
        """
            Function to make all calculation
            :@param kind: Define which element we are working for
            :@type kind: string
            :@default kind: BEAM

            kind can be:
                - BEAM
                - SLAB
                - WALL
        """
        self.__section_kind = kind

        self.vrdc, self.vrdc_1, self.vrdc_2, self.vmin = \
                vrdc(self.__mat_concrete.fck, self.__mat_concrete.GAMMA_C, \
                    self.__section.area, self.__section.d, self.__section.b, \
                    self.__section.ast, kind, self.__nedu, True)

        self.theta, self.__cot_theta = theta(self.__mat_concrete.fcd, self.nu,\
                self.__vedu_red, self.__section.b, self.__section.z)
        self.__define_vrdmax()
        self.__deifne_asw_s()

        self.__define_simga_rdc()
        self.__define_as_support()

        self.__define_roh_min()
        self.__define_asw_min()

        self.__define_st_max()
        self.__define_sl_max()

    def define_ved_red(self, P, kind="UNIFORM", length=0):
        """
            function to define ved_red
            :@param P: force use for the reduction
            :@param kind: type of the force, to reduce the right way
            :@param length: distance of the reduction
            :@type P: double
            :@type kind: string
            :@type length: double
            :@default kind: UNIFORM (if we want to reduce an uniforme load)
            :@default length: 0 (if we don't put a length, Ved is not reduce)

            kind could b:
                - UNIFORM
                - PONCTUAL

            the length have to be:
                - d = near to support
                - z * cot_theta = otherwise
        """
        if kind == "UNIFORM":
            self.__vedu_red = self.__vedu - P * length

    def __define_vrdmax(self):
        """ function to define vrdmax """
        fck = self.__mat_concrete.fck
        fcd = self.__mat_concrete.fcd

        self.nu = 0.6 * (1 - fck / 250)

        self.vrdmax = (self.nu * fcd * self.__b * self.__z * \
                (self.__cot_theta + self.__cot_alpha) * \
                self.alpha_cw) / (1 + self.__cot_theta**2)

    def __deifne_asw_s(self):
        """ fucntion to define asw/s """
        fyd = self.__mat_steel.fyk / self.__mat_steel.GAMMA_S

        sin_alpha = math.sin(math.radians(self.__alpha))

        devid = fyd * self.__z * (self.__cot_theta + self.__cot_alpha) * \
                sin_alpha

        self.asw_s = self.__vedu_red / devid

    def __define_simga_rdc(self):
        """ function to define simga_rdc """
        theta_p = mpmath.acot((self.__section.al + self.__z * \
                self.__cot_theta - self.__section.cnom) / (2 * self.__z))
        sin_theta_p = math.sin(theta_p)

        self.sigma_rdc = self.__vedu / (self.__b * self.__section.al * \
                sin_theta_p**2)

    def __define_as_support(self):
        """ function to define As support """
        cot_theta_p = (self.__section.al + self.__z * \
                self.__cot_theta - self.__section.cnom) / (2 * self.__z)

        al = self.__z * (cot_theta_p - self.__cot_alpha)

        self.fe = self.__vedu * al / self.__z + self.__nedu + \
                self.__medu / self.__z

        sigma_st = self.__mat_steel.fyk / self.__mat_steel.GAMMA_S

        self.as_support = self.fe / sigma_st

    def __define_roh_min(self):
        """ function to define roh,min """
        fck = self.__mat_concrete.fck
        fyk = self.__mat_steel.fyk

        sin_alpha = math.sin(math.radians(self.__alpha))

        self.roh_min = 0.08 * math.sqrt(fck) * self.__b * sin_alpha / fyk

    def __define_asw_min(self):
        """ function to define asw_min """
        sin_alpha = math.sin(math.radians(self.__alpha))

        self.asw_min = self.__b * self.roh_min * sin_alpha

    def __define_st_max(self):
        """ function to define the transversal space between steel """
        self.st_max = min(0.75 * self.__d, 0.600) # 600 m => 0.6 m

    def __define_sl_max(self):
        """ function to defnie the longitudinal space between steel """
        self.sl_max = 0.75 * self.__d * (1 - self.__cot_alpha)

    def calculation_note_fr(self, name, office="WORD"):
        """ Function to create calculation note """
        pass
      #  my_doc = TWord.TWord(name, office)
       # my_doc.create()

if __name__ == "__main__":
    file = __file__
    file = file.replace("shear.py","")
    sys.path.append(file+'../../')
    from section.section import Rect
    from section.material import MatConcrete, MatSteel
    b = 0.8
    h = 1
    fck = 30
    fyk = 500
    section = Rect(b, h, "BA")
    concrete = MatConcrete(fck)
    steel = MatSteel(fyk)

    section.ast = 50 * 10**(-4)
    section.asc = 0
    section.z = 0.9 * 0.9 * h
    section.ALPHA_SHEAR = 90

    Ved = 1 # MN
    test = Shear(Ved, section, steel, concrete)
    test.make_calculation()

    print("theta: ", test.theta)
