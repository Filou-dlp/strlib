#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to calculate the flexion in steel structure
"""
from flexion_det import *

__all__ = ['Flexion', 'ml_rd']

class Flexion:
    """
        Class to calculate flexion in steel structure
    """
    
    def __init__(self, Med, wl, fy, gamma_m0):
        """
            Constructor and calculate ml_rd

            :@param Med: bending moment
            :@param wl: static moment of the section can be:
                - Wpl: Class 1 and 2
                - Wel: Class 3
                - Weff: Class 4
            :@param fy: resistance of the element
            :@param gamma_m0: security coef for steel
            :@type Med: float
            :@type wl: float
            :@type fy: float
            :@type gamma_m0: float
        """
        self.__med = Ned
        self.ml_rd = ml_rd(wl, fy, gamma_m0)
    
    def verification(self):
        """ 
            return Med/Ml,rd
            Ml,rd can be:
                - Mpl,rd
                - Mel,rd
                - Meff,rd
            must be < 1 (to be correct)
        """
        return self.__med / self.ml_rd 