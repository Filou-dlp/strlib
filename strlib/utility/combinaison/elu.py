#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to realise all combinaison calculation
"""
from typing import Tuple

import sys
import math

from itertools import permutations, combinations, product

__version__ = 0.4

class Combinaison:
    """
        Class to calculate all possible combinaison from Eurocode
    """

    GAMMA_G_ELU_STR_GEO_FAV: float = 1
    GAMMA_P_ELU_STR_GEO_FAV: float = 1
    GAMMA_Ad_ELU_STR_GEO_FAV: float = 1.5
    GAMMA_Q_ELU_STR_GEO_FAV: float = 1.5

    GAMMA_G_ELU_STR_GEO_DEFAV: float = 1.35
    GAMMA_P_ELU_STR_GEO_DEFAV: float = 1.35
    GAMMA_Ad_ELU_STR_GEO_DEFAV: float = 1.5
    GAMMA_Q_ELU_STR_GEO_DEFAV: float = 1.5

    GAMMA_G_ELS_CAR: float = 1
    GAMMA_P_ELS_CAR: float = 1
    GAMMA_Ad_ELS_CAR: float = 1
    GAMMA_Q_ELS_CAR: float = 1

    def __init__(self, list_G: tuple, list_Q: Tuple[Tuple[float, float]], list_P: tuple = (), list_Ad: tuple = ()):
        """
            Constructor
            :@param list_G: list of Permanent load
            :@param list_Q: ( ([VAL], [Coef]), ([VAL], [Coef]) )
            :@param list_P: list of prestress load
            :@param list_Ad: list of accidental load
            :@type list_G: tuple
            :@type list_Q: tuple(tuple)
            :@type list_P: tuple
            :@type list_Ad: tuple
            :@default list_P: ()
            :@default list_Ad: ()

        """
        self.__list_G: tuple = list_G
        self.__list_P: tuple = list_P
        self.__list_Ad: tuple = list_Ad

        self.__list_Q: tuple = list_Q

    def __add_load(self, value: tuple, coef: float):
        """ function to calcul G/P/Ad in the combinaison
            :@param value: tuple of all value
            :@type value: tuple

            :@return rslt: rslt, numerical value of the element
            :@type rslt: float

            Exemple:
            value = (40, 50)
            coef = GAMMA_G_STR_GEO_DEFAV (1,35)

            rslt = 40 * 1,35 + 50 * 1,35
        """
        rslt: float = 0
        for i in value:
            rslt += i * coef
        return rslt

    def __add_variable(self, value: tuple, coef: float):
        """ Fonction sum product for value and coef 
            Eurocod combinaison
            :@param value: Value of the load and the phy_coef according to eurocod
            :@param coef: Coefficient for multiplication
            :@type value: tuple(tuple)
            :@type coef: float

            :@return rslt: value of the sum product
            :@type rslt: float

            Exemple:
            value = ( (25, 0.7), (40, 0.5) )
            rslt = 1.5 * 25 + 40 * 1.5 * 0.5
        """
        rslt = 0
        first = False
        for val, phy_coef in value:
            if not first:
                rslt += val * coef
                first = True
            else:
                rslt += val * phy_coef * coef
        return rslt

    def __make_combinaison(self, coef: Tuple[float]):
        """ function to make all possible combinaison with different value

            :@param coef: list of coef for the combinaison type
            :@type coef: tuple

            :@return comb: list of all combinaison
            :@type comb: list

            Exemple:
            coef = (1.35, 1, 1, 1.5)
            G, Q, S
            1.35G + 1.5Q + 1.5 * phy * S
            1.35G + 1.5S + 1.5 * phy * Q
            1.35G + 1.5Q
            1.35G + 1.5S
            1.35G + 1.5 * phy * S
            1.35G + 1.5 * phy * Q
            1.35G
        """
        coef_G = coef[0]
        coef_P = coef[1]
        coef_Ad = coef[2]
        coef_Q = coef[3]

        G: float = self.__add_load(self.__list_G, coef_G) if self.__list_G else 0
        P: float = self.__add_load(self.__list_P, coef_P) if self.__list_P else 0
        Ad: float = self.__add_load(self.__list_Ad, coef_Ad) if self.__list_Ad else 0

        comb = []
        Q_list = list(permutations(self.__list_Q))
        for i in range(0, len(Q_list)):
            Q: float = self.__add_variable(Q_list[i], coef_Q)
            comb.append(G + P + Ad + Q)

        var_list_Q = list(self.__list_Q)
        counter = 0
        for ii in range(0, len(self.__list_Q) **2 - 1):
            if ii == len(self.__list_Q):
                var_list_Q = list(self.__list_Q)
                counter = ii - 1
            var_list_Q[counter] = (0, 0)
            Q_list =list(permutations(var_list_Q))
            for i in range(0, len(Q_list)):
                Q: float = self.__add_variable(Q_list[i], coef_Q)
                comb.append(G + P + Ad + Q)
            counter += 1

        return comb

    def ulu_equ_favorable(self):
        """ function to calculate combinaison """
        raise NotImplementedError

    def ulu_equ_defavorable(self):
        """ function to calculate combinaison """
        raise NotImplementedError

    def ulu_str_geo_favorable(self):
        """ function to calculate combinaison """
        coef = (self.GAMMA_G_ELU_STR_GEO_FAV, self.GAMMA_P_ELU_STR_GEO_FAV,
                self.GAMMA_Ad_ELU_STR_GEO_FAV, self.GAMMA_Q_ELU_STR_GEO_FAV)
        return self.__make_combinaison(coef)
    
    def ulu_str_geo_defavorable(self):
        """ function to calculate combinaison """
        coef = (self.GAMMA_G_ELU_STR_GEO_DEFAV, self.GAMMA_P_ELU_STR_GEO_DEFAV,
                self.GAMMA_Ad_ELU_STR_GEO_DEFAV, self.GAMMA_Q_ELU_STR_GEO_DEFAV)
        return self.__make_combinaison(coef)

    def ulu_sis_newmark(self):
        """ function to calculate combinaison """
        raise NotImplementedError

    def uls_char(self):
        """ function to calculate combinaison """
        coef = (self.GAMMA_G_ELS_CAR, self.GAMMA_P_ELS_CAR,
                self.GAMMA_Ad_ELS_CAR, self.GAMMA_Q_ELS_CAR)
        return self.__make_combinaison(coef)

    def uls_freq(self):
        """ function to calculate combinaison """
        raise NotImplementedError

    def uls_qp(self):
        """ function to calculate combinaison """
        raise NotImplementedError


if __name__ == "__main__":
    G = 40,
    Q = ( (25, 0.7), (40, 0.5) )

    Test = Combinaison(G, Q)

    rslt = Test.ulu_str_geo_favorable()
    print(rslt)
