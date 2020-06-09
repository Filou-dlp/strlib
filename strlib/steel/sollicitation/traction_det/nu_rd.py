#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Calculate Nu,rd for steel
"""

def nu_rd(net_area, fu, gamma_m2, beta=0.9):
    """
        :@param net_area: Net area (when there is bolt hole)
        :@param fu: traction resistance of the section
        :@param gamma_m2: security coef for steel
        :@param beta: coefficient depending of the bolt number
        :@type net_area: float
        :@type fu: float
        :@type gamma_m2: float
        :@type beta: float
        :@default beta: 0.9
    """
    return beta * net_area * fu / gamma_m0