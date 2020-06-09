#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Calculate Nc,rd for steel
"""

def nc_rd(area, fy, gamma_m0):
    """
        :@param area: area of the section
        :@param fy: resistance of the section
        :@param gamma_m0: security coef for steel
        :@type area: float
        :@type fy: float
        :@type gamma_m0: float
    """
    return area * fy / gamma_m0