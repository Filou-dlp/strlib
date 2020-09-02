#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module allow to make calculation for the shear force
"""
import sys
print(__name__)
sys.path.append((__file__).replace("theta.py","")+"../../../")
from math import radians, asin, tan

from Aide.return_class import float_choice_index

def theta(__fcd, __nu, __vedu_red, __b, __z):
    """ function to define theta """
    theta_rad = 1 / 2 * asin(2 * __vedu_red / \
            (__b * __z * __nu * __fcd))

    if theta_rad <= radians(21.8):
        theta = 21.8
    elif theta_rad >= radians(45):
        theta = 45
    else:
        theta = radians(theta_rad)

    cot_theta = 1 / (tan(radians(theta)))

    print("cot_theta: ", cot_theta)
    print("theta: ", theta)

    return float_choice_index(theta, cot_theta)


if __name__ == "__main__":
    test = theta(20, 0.528, 1, 0.8, 0.8)