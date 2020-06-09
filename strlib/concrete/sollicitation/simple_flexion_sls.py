#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to make simple flexion SLS calculation
"""
import sys
import math

sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
import TWord

class SimpleFlexureSLS:
    """
        Class to calculate element in simple flexure SLS
    """
    def __init__(self, meds, medu, cross_section, mat_steel, mat_concrete):
        """ Constructor
            :@param Meds: Moment inside the section
            :@param cross_section: section of the element
            :@param mat_steel: property of the reinforce steel
            :@param mat_concrete: property of the concrete
            :@type Medu: double
            :@type cross_section: TSection object
            :@type mat_steel: TMaterial object
            :@type mat_concrete: TMaterial object
        """

        self.__m_eds = meds
        self.__m_edu = medu

        self.__mat_steel = mat_steel
        self.__mat_concrete = mat_concrete

        self.__section = cross_section

    def make_calculation(self, fcs, fys, kind="RECT", d=0, d_p=0):
        """
            function to make all calculation
            :@param fcs: stress in the concrete
            :@param fys: stress in the steel
            :@param kind: type of secion to make calculation
            :@param d: usefull heigth for tensil reinforcement
            :@param d_p: usefull heigth for compression reinforcement
            :@type fcs: double
            :@type fys: double
            :@type kind: string
            :@type d: double
            :@type d_p: double
            :@default kind: RECT (mean rectangulare section, RANDOM for a random section)
            :@default d: 0 (take the default value .9*h)
            :@default d_p: 0 (take the default value .1*h)
        """

        self.__fcs = fcs
        self.__fys = fys

        self.__alpha_e = 0

        if kind == "RECT":

            self.__seciton_kind = "RECT"

            h_ = self.__section.h
            self.__d = self.__section.d if d == 0 else d
            self.__d_p = self.__section.d_p if d_p == 0 else d_p

            self.__define_mu_ab()
            self.__define_mu_eds()
            self.__define_mu_lim()
            self.__define_chi_eds()
            self.__z_eds()
            self.__sigma_st()
            self.__define_Ast()

            if self.__mu_eds > self.__mu_lim:
                self.__sigma_st()
                self.__define_Ast()

            self.__mecanical_ratio()
            self.__geometrical_ratio()

        elif kind == "RANDOM":
            pass

    def __define_mu_ab(self):
        """ Functon to define mu_ab """
        theta_y_ = self.__alpha_e * self.__fcs / self.__fys

        alpha_ab_ = theta_y_ / (1 + theta_y_)

        self.__mu_ab = alpha_ab_ * (3 - alpha_ab_) / 6

    def __define_mu_lim(self):
        """
            Function to define mu_lim
            aproached function
        """
        gamma_ = self.__m_edu / self.__m_eds
        fck_ = self.__mat_concrete.fck_
        divid_ = (4.69-1.7 * gamma_) * fck_ + (159.9 - 76.2 * gamma_)
        self.__mu_lim = fck_ / divid_

    def __define_mu_eds(self):
        """
            function to define mu_eds
            with/without compressive reinforcement
        """
        b_ = self.__mat_concrete.b

        self.__mu_eds = self.__m_eds / (b_ * (self.__d**2) * fcs)

        if self.__mu_eds > self.__mu_lim:
            self.__mu_eds_com = self.__mu_eds - self.__mu_lim
            self.__mu_eds = self.__mu_lim

            self.__M_lim = self.__mu_eds * b_ * self.__d**2 * self.__fcs

    def __define_chi_eds(self):
        """
            Function to define chi_eds
            with/without compressive reinforcement
        """
        if self.__mu_eds < self.__mu_lim:
            if self.__mu_eds <= self.__mu_ab:
                r_ = math.sqrt(1 + 2 * self.__mu_eds)
                theta_ = math.acos(1 / r**3) / 3

                self.__chi_eds = 1 + 2 * r_ * \
                        math.cos(theta_ - 2 * math.pi / 3)
            else:
                self.__chi_eds = 3 * (1 - math.sqrt(1 - 8 * self.__mu_eds / 3)) / 2

        else:
            self.__chi_eds = 3 * (1 - math.sqrt(1 - 8 * self.__mu_eds / 3)) / 2
            self.__chi_eds_com = 3 * (1 - \
                    math.sqrt(1 - 8 * self.__mu_eds_com / 3)) / 2

    def __define_z_eds(self):
        """
            Function to define z
            with/without compressive reinforcement
        """
        if self.__mu_eds < self.__mu_lim:
            self.__z_eds = d * (1 - self.__chi_eds / 3)
        else:
            self.__z_eds = d * (1 - self.__chi_eds / 3)
            self.__z_eds_com = self.__d - self.__d_p

    def __define__sigme_st(self):
        """ Function to define sigmat_st """
        if self.__mu_eds <= self.__mu_ab:
            self.__sigma_st = self.__fys

        else:
            self.__sigma_st = self.__alpha_e * self.__fcs * \
                    (1 - self.__chis_eds) / self.__chi_eds

    def __define_sigma_sc(self):
        """ Function to define sigmat_sc """
        delta_ = self.__d_p / self.__d
        self.__sigma_sc = self.__alpha_e * (self.__chi_eds_com - delta_) * \
                self.__fcs / self.__chi_eds_com

    def __define_Ast(self):
        """
            Function to define Ast
            with/without compression reinforcement
        """
        self.__ast = self.__m_eds / (self.__z_eds  * self.__sigma_st)
        if self.__mu_eds > self.__mu_lim:
            self.__ast += (self.__m_eds - self.__M_lim) / \
                    (self.__z_eds_com * self.__sigma_st)

    def __define_Asc(self):
        """
            Function to define Asc
            with compression reinforcement
        """
        self.__asc = (self.__Med_eds - self.__M_lim) / \
                (self.__z_eds_com * self.__sigma_sc)

    def __mecanical_ratio(self):
        """
            Function to define
            without compressive reinforcement
        """
        if self.__mu_eds <= self.__mu_lim:
            self.__omega_st = (self.__chi_eds**2) / (2 * (1 - self.__chi_eds))

        else:
            self.__omega_st = 0
            self.__omega_sc = 0

    def __geometrical_ratio(self):
        """
            Function to define
            with/without compressive reinforcement
        """
        if self.__mu_eds <= self.__mu_lim:
            self.__roh = self.__omega_st / self.__alpha_e

        else:
            Area_ = self.__section.Area
            self.__roh = (self.__ast + self.__asc) / Area_

# Set

    def __set_alpha_e(self, val):
        self.__alpha_e = val

# Get
    def __get__d(self):
        return self.__d
    def __get_d_p(self):
        return self.__d_p

    def __get_alpha_e(self):
        return self.__alpha_e

    def __get_mu_ab(self):
        return self.__mu_ab
    def __get_mu_lim(self):
        return self.__mu_lim
    def __get_mu_eds(self):
        return self.__mu_eds

    def __get_mu_eds_com(self):
        return self.__mu_eds_com

    def __get_z_eds(self):
        return self.__z_eds
    def __get_z_eds_com(self):
        return self.__z_eds_com

    def __get_M_lim(self):
        return self.__M_lim

    def __get_sigma_st(self):
        return self.__sigma_st
    def __get_sigma_sc(self):
        return self.__sigma_sc

    def __get_Ast(self):
        return self.__ast
    def __get_Asc(self):
        return self.__asc

    def __get_omega_st(self):
        return self.__omega_st
    def __get_omega_sc(self):
        return self.__omega_sc

    def __get_roh(self):
        return self.__roh

# Property

    d = property(__get__d)
    d_p = property(__get_d_p)

    alpha_e = property(__get_alpha_e, __set_alpha_e)

    mu_ab = property(__get_mu_ab)
    mu_lim = property(__get_mu_lim)
    mu_eds = property(__get_mu_eds)
    mu_eds_com = property(__get_mu_eds_com)

    z_eds = property(__get_z_eds)
    z_eds_com = property(__get_z_eds_com)

    M_lim = property(__get_M_lim)

    sigma_st = property(__get_sigma_st)
    sigma_sc = property(__get_sigma_sc)

    Ast = property(__get_Ast)
    Asc = property(__get_Asc)

    omega_st = property(__get_omega_st)
    omega_sc = property(__get_omega_sc)

    roh = property(__get_roh)

