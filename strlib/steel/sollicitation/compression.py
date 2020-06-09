#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to calculate compression for steel structure
"""
from compression_det import *

__all__ = ['Compression', 'nc_rd']

class Compression:
    """
        Class to calculate compression in steel structure
    """
    
    def __init__(self, Ned, area, fy, gamma_m0):
        """ 
            Constructor and calculate Nc,rd

            :@param Ned: normal force
            :@param area: area of the element can be
                - Area: Class 1,2 and 3
                - Aeff: Class 4
            :@param fy: resistance of the element
            :@param gamma_m0: security coef for steel
            :@type Ned: float
            :@type area: float
            :@type fy: float
            :@type gamma_m0: float
        """
        self.__ned = Ned
        self.nc_rd = nc_rd(area, fy, gamma_m0)
    
    def verification(self):
        """
            return Ned/Nc,rd
            must be < 1 (to be correct)
        """
        return self.__ned / self.nc_rd 

if __name__=="__main__":
    pass