#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module docstring
"""
import sys
import math

#sys.path.append(sys.path[0]+'/../Office_lib')
#print(sys.path)
#import TWord 


class Spacing:
    """
        Docstring
    """
    SPACE_PHY_Y_PHY_L = 10 # mm
    K1 = 1
    K2 = 5 # mm

    def __init__(self, b, cnom, phy_t, phy_l, dg):
        """
            Constructor
            :@param h:
            :@param cnom:
            :@param phy_t:
            :@param phy_l:
            :@param dg:
            
        """
        self.__b = b
        self.__cnom = cnom
        self.__phy_t = phy_t
        self.__phy_l = phy_l
        self.__dg = dg
        self.__define_eh()
        self.__define_e_min()
    
    def __define_eh(self):
        """ function to define horizontal spacement """
        self.eh = (self.__b - 2 * self.__cnom - 2 * self.__phy_t - \
                2 * self.SPACE_PHY_Y_PHY_L - self.__phy_l[0] / 2 - 
                self.__phy_l[-1] / 2 ) / (len(self.__phy_l) - 1)

    def __define_e_min(self):
        """ function to define the minimum of the horizontal/vertical spacement """
        v1 = self.K1 * max(self.__phy_l)
        v2 = max(self.__dg * self.K2, 20) # mm
        self.eh_min = max(v1, v2)
        self.ev_min = max(v1, v2)


if __name__ == "__main__":
    h = 400 
    cnom = 35
    phy_t = 8
    phy_l = (25, 25, 25, 25, 25)
    test = Spacing(h, cnom, phy_t, phy_l)
    print(test.eh)
