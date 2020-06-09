#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to calculated traction in steel structure
"""
from traction_det import *

__all__ = ['Traction', 'npl_rd', 'nu_rd', 'nnet_rd']

class Traction:
    """
        Class to calculate traction in steel structure
    """

    def __init__(self, Ned, area, net_area, fy, fu, gamma_m0, gamma_m2,\
        beta=0.9):
        """ 
            Constructor and calculate:
                - Npl,rd
                - Nu,rd
                - Nnet,rd
            
            :@param Ned: Normal force
            :@param area: area of the section can be:
                - Area: Class 1, 2 and 3
                - Aeff: Class 4
            :@param net_area: Net area (when there is bolt hole)
            :@param fy: resistance of the section
            :@param fu: traction resistance of the section
            :@param gamma_m0: security coef for steel
            :@param gamma_m2: security coef for steel
            :@param beta: coefficient for nu,rd
            :@type Ned: float
            :@type area: float
            :@type net_area: float
            :@type fy: float
            :@type fu: float
            :@type gamma_m0: float
            :@type gamma_m2: float
            :@type beta: float
            :@default beta: 0.9
        """
        self.__ned = Ned
        self.npl_rd = npl_rd(area, fy, gamma_m0)
        self.nu_rd = nu_rd(net_area, fu, gamma_m2, beta)
        self.nnet_rd = nnet_rd(net_area, fy, gamma_m0)
        self.nrd = min(self.npl_rd, self.nu_rd, self.nnet_rd)
    
    def verification(self):
        """ 
            return Ned/Nrd
            must be < 1 (to be correct)
        """
        return self.__ned / self.nrd 


if __name__ == "__main__":
    test = Traction(40, 10, 5, 235, 200, 1)
    print(test.npl_rd)
    print(test.nu_rd)
    print(test.nnet_rd)
