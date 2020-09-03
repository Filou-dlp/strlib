#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module allow to make calculation for the shear force
"""

import sys
sys.path.append((__file__).replace("vrdc.py","")+"../../../")
from math import sqrt

#from Aide.return_class import float_choice_index

def vrdc(__fck, __gamma_c, __area, __d, __b, __asl, __kind="BEAM", __nedu=0,\
        return_arg=False):
        """
            function to define vrdc
            Vrdc,1; Vrdc,2 and vmin can be return if need
            :@param __fck:
            :@param __gamma_c:
            :@param __nedu:
            :@param __area:
            :@param __d:
            :@param __b:
            :@param __asl:
            :@param __kind:
            :@type __fck: integer
            :@type __gamma_c: doule
            :@type __nedu: float
            :@type __area:
            :@type __d:
            :@type __b:
            :@type __asl:
            :@type __kind:
            :@default __nedu: 0 (mean no prestress)
            :@default __kind: BEAM ()

            possible value for kind:
            - Beam
            - Slab
            - Wall
        """
        # prestress
        k1 = 0.15
        sigma_cp = min(__nedu / __area, 0.2)

        # Vrdc,1
        crdc = 0.18 / __gamma_c
        k = 1 + sqrt(.200 / __d) # 200 mm = 0.2 m

        roh_l = __asl / (__b * __d)

        vrdc_1 = crdc * k * (100 * roh_l * __fck)**(1/3) + k1 * sigma_cp

        # Vrdc,2
        if __kind == "BEAM":
            vmin = 0.053 / __gamma_c * k**(1.5) * __fck**(0.5)
        elif __kind == "SLAB":
            vmin = 0.34 / __gamma_c * __fck**(0.5)
        elif __kind == "WALL":
            vmin = 0.35 / __gamma_c * __fck**(0.5)

        vrdc_2 = vmin + k1 * sigma_cp

        # Vrdc
        vrdc = max(vrdc_1, vrdc_2) * __b * __d

        print("vrdc_1: ", vrdc_1)
        print("vrdc_2: ", vrdc_2)
        print("vmin: ", vmin)
        print("vrdc: ", vrdc)

        if return_arg:
            return vrdc, vrdc_1, vrdc_2, vmin
        else:
            return vrdc
        
if __name__ == "__main__":
    pass