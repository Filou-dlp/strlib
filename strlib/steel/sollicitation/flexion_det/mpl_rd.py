#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Calculate Ml,rd for steel, can be:
        - Mpl,rd
        - Mel,rd
        - Meff,rd
"""

def ml_rd(wl, fy, gamma_m0):
    """
        :@param wl: static moment can be
            - Wpl
            - Wel
            - Weff
        :@param fy: resistance of the section
        :@param gamma_m0: security coef for steel
        :@type wl: float
        :@type fy: float
        :@type gamma_m0: float
    """
    return wl * fy / gamma_m0