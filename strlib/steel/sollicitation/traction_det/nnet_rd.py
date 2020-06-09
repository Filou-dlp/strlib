#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Calculate Nnet,rd for steel
"""

def nnet_rd(net_area, fy, gamma_m0):
    """
        :@param net_area: Net area (when there is bolt hole)
        :@param fy: resistance of the section
        :@param gamma_m0: security coef for steel
        :@type net_area: float
        :@type fy: float
        :@type gamma_m0: float
    """
    return net_area * fy / gamma_m0