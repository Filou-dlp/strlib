#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define the shinkrage of a section
"""
import sys
import math

sys.path.append(sys.path[0]+'/../../Office_lib')
print(sys.path)
# import TWord 


class Shinkrage:
    """
        Class to calculate the shinkrage of a section
    """
    
    RH_0 = 100 # EC Annexe B eq B.11
    FCM0 = 10 # EC Annexe B eq B.11
    RH = 70

    def __init__(self, fck, t, ts, Ac, u, cement_class="N", RH=70):
        """
            Constructor
            :@param fck:
            :@param t:
            :@param ts:
            :@param Ac:
            :@param u:
            :@param cement_class:
            :@param RH:
        """
        # Variable that will be used
        self.__fck = fck
        self.__fcm = fck + 8
        self.__ac = Ac
        self.__u = u
        self.__t = t
        self.__ts = ts
        if RH != 70:
            self.RH = RH
        if cement_class == "S":
            self.alpha_ds1 = 3
            self.alpha_ds2 =  0.13
        elif cement_class == "N":
            self.alpha_ds1 = 4
            self.alpha_ds2 =  0.12
        elif cement_class == "R":
            self.alpha_ds1 = 6
            self.alpha_ds2 =  0.11
        
        self.__define_value()

    def __define_value(self):
        """ function to define all value """
        self.__define_h0()
        self.__define_kh()
        self.__define_beta_ds_t_ts()
        self.__define_beta_RH()
        self.__define_epsilon_cd_0()
        self.__define_dessiccation_shinkrage()

        self.__define_beta_as_t()
        self.__define_epsilon_ca_inf()
        self.__define_epsilon_ca_t()

        self.__define_total_shinkrage() 

    # Dissiccation
    def __define_h0(self):
        """ function to define h0 """
        self.h0 = 2 * self.__ac / self.__u * 1000

    def __define_kh(self):
        """ function to define kh """
        if self.h0 <= 100:
            self.kh = 1
        elif self.h0 > 100 and self.h0 <= 200:
            self.kh = 1 + (self.h0 - 100) * (0.85 - 1) / (200 - 100)
        elif self.h0 > 200 and self.h0 <= 300:
            self.kh = 0.85 + (self.h0 - 200) * (0.75 - 0.85) / (300 - 200)
        elif self.h0 > 300 and self.h0 <= 500:
            self.kh = 0.75 + (self.h0 - 500) * (0.70 - 0.75) / (500 - 300)
        elif self.h0 > 500:
            self.kh = 0.70

    def __define_beta_ds_t_ts(self):
        """ function to define beta_ds(t,ts) """
        self.beta_ds_t_ts = (self.__t - self.__ts) / ((self.__t - self.__ts) + 0.04 * math.sqrt(self.h0**3))

    def __define_beta_RH(self):
        """ function to define beta_RH """
        self.beta_rh = 1.55 * (1 - (self.RH / self.RH_0)**3)
    
    def __define_epsilon_cd_0(self):
        """ function to define epsilon_cd_0 """
        self.epsilon_cd_0 = 0.85 * ((220 + 110 * self.alpha_ds1) * math.exp(-self.alpha_ds2 * self.__fcm / self.FCM0)) * 10**(-6) * self.beta_rh
    
    def __define_dessiccation_shinkrage(self):
        """ function to define epsilon_cd(t) which is the dessictation shinkrage """
        self.epsilon_cd_t = self.beta_ds_t_ts * self.kh * self.epsilon_cd_0

    # Endogenous
    def __define_beta_as_t(self):
        """ function to define beta_as(t) """
        self.beta_as_t = 1 - math.exp(-0.2 * self.__t **0.5)
    
    def __define_epsilon_ca_inf(self):
        """ function to define epsilon_ca(inf) """
        self.epsilon_ca_inf = 2.5 * (self.__fck - 10) * 10**(-6)

    def __define_epsilon_ca_t(self):
        """ function to define epsilon_ca(t) """
        self.epsilon_ca_t = self.beta_as_t * self.epsilon_ca_inf

    # total
    def __define_total_shinkrage(self):
        """ function to define total shinkrage """
        self.epsilon_cs = self.epsilon_cd_t + self.epsilon_ca_t

    def calculation_note_fr(self, name, kind="WORD"):
        """ function to generate a calculation note """
        pass

if __name__ == "__main__":
    pass
 
 
