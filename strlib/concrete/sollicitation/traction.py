 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module docstring
"""
import sys
import math

sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
import TWord

class Traction:
    """
        docstring
    """

    def __init__(self, Ned, cross_section, mat_steel, mat_concrete, sigma_s=0):
        """
            Constructor
        """
        self.__n_eds = Ned

        self.__mat_steel = mat_steel
        self.__mat_concrete = mat_concrete

        self.__section = cross_section

        self.__sigma_s = sigma_s if sigma_s == 0 else self.__mat_steel.fyk
        
        # Variable that will be used
        
    def make_calculation(self):
        """ function to make calculation """
        self.__define_As()
        self.__define_asmin()
        
    def __define_As(self):
        """ Function to define As """
        self.__As = self.__n_eds / self.__sigma_s

    def __define_asmin(self):
        """ Function to define Asmin """
        Ac = self.__mat_concrete.Ac
        fctm_ = self.__mat_concrete.fctm
        fyk_ = self.__mat_steel.fyk
        self.__asmin = Ac / (fyk_ * fctm_)

    def calculation_note_fr(self):
        """ docstring """

    @staticmethod
    def construction_min(self):
        """
            Function to define construction min
            see below

            phy_t >= phy_L/3
            s_t <= a
        """
