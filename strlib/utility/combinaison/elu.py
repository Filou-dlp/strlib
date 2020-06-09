#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to realise all combinaison calculation
"""
import sys
import math

from itertools import permutations, combinations, product

#sys.path.append(sys.path[0]+'/../Office_lib')
#print(sys.path)
#import TWord 


class Combinaison:
    """
        Docstring
    """

    def __init__(self, list_G, lisg_Q):
        """
            Constructor
        """

    @staticmethod
    def ulu_equ_g_favorable(g, q, s, coef_q, coef_s):
        """ """
        G = 1.15 * g

        prod = product(coef_q, coef_s)
        
        my_list = []

        for i in prod:
            my_list.append(i)

        my_list.pop()
        tmp = len(my_list)
        del my_list[int(tmp/2)]

        comb = []

        for i in my_list:
            tmp = G + i[0]*q + i[1]*s
            comb.append(tmp)
        
        return comb


    def ulu_equ_g_defavorable(self):
        """ """
        pass

    def ulu_str_geo_g_favorable(self):
        """ """
        pass
    
    def ulu_str_geo_g_defavorable(self):
        """ """
        pass

    def ulu_sis_newmark(self):
        """ """
        pass

    def uls_char(self):
        """ """
        pass

    def uls_freq(self):
        """ """
        pass

    def uls_qp(self):
        """ """
        pass
        
        # Variable that will be used


if __name__ == "__main__":
    list1 = (0, 0.7, 1.5)
    list2 = (0, 0.75, 1.5)

    Combinaison.ulu_equ_g_favorable(20, 100, 50,list1, list2)