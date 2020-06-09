#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Calculate Npl,rd for steel
"""

def npl_rd(area, fy, gamma_m0):
    """
        :@param area: area of the section, can be:
            - Area: Class 1, 2 and 3
            - Aeff: Class 4
        :@param fy: resistance of the section
        :@param gamma_m0: security coef for steel
        :@type area: float
        :@type fy: float
        :@type gamma_m0: float
    """
    return area * fy / gamma_m0