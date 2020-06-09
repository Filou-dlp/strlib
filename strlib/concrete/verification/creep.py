 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define the creep of a section
"""
import sys
import math

# sys.path.append(sys.path[0]+'/../../Office_lib')
# print(sys.path)
# import TWord 

class Creep:
    """
        Class for the creep
        this class don't take into account:

        - t0 modify in function of the ciment EC2 Annex B eq B9
        - t0 modify in function of the temperature EC2 Annex B eq B10
    """
    RH = 70

    def __init__(self, fck, t, t0, Ac, u, RH=70):
        """
            Constructor
            :@param fck: resitance of the material
            :@param t: age of the concrete at the time we want
            :@param t0: age of the concrete when we put load
            :@param Ac: section of the element
            :@param u: perimeter of the element in contact of the air
            :@param RH: % of humidity
            :@type fck: double
            :@type t: double
            :@type t0: double
            :@type Ac: double
            :@type u: double
            :@type RH: double
            :@default RH:
        """
        # Variable that will be used
        self.__fcm = fck + 8
        self.__Ac = Ac
        self.__u = u
        self.__t = t
        self.__t0 = t0
        if RH != 70:
            self.RH = RH
         
        self.__define_value()
    
    def __define_value(self):
        """ function to define all value """
        self.__define_alpha_i()
        self.__define_h0()
        self.__define_phy_RH()
        self.__define_beta_fcm()
        self.__define_beta_t0()
        self.__define_beta_h()
        self.__define_beta_c_t_t0()
        self.__define_phy_0()
        self.__define_phy_t_t0()

    def __define_alpha_i(self):
        """ function to define alpha_1, alpha_2, alpha_3 """
        self.alpha_1 = (35 / self.__fcm)**0.7
        self.alpha_2 = (35 / self.__fcm)**0.2
        self.alpha_3 = (35 / self.__fcm)**0.5

    def __define_h0(self):
        """ function to define h0 """
        self.h0 = 2 * self.__Ac / self.__u * 1000

    def __define_phy_RH(self):
        """ function to define phy_RH """
        if self.__fcm <= 35:
            self.phy_rh = 1 + (1 - self.RH / 100) / (0.1 * self.h0**(1/3))
        else:
            self.phy_rh = (1 + (1 - self.RH / 100) * self.alpha_1 / (0.1 * self.h0**(1/3))) * self.alpha_2

    def __define_beta_fcm(self):
        """ function to define beta(fcm) """
        self.beta_fcm = 16.8 / math.sqrt(self.__fcm)

    def __define_beta_t0(self):
        """ funtion to define beta(t0) """
        self.beta_t0 = 1 / (0.1 + self.t0**0.2)

    def __define_beta_h(self):
        """ function to define beta_h """
        if self.__fcm <= 35:
            self.beta_h = min(1.5 * (1 + (0.012 * self.RH)**18) * self.h0 + 250, \
                1500)
        else:
            self.beta_h = min(1.5 * (1 + (0.012 * self.RH)**18) * self.h0 + 250 * self.alpha_3, \
                1500 * self.alpha_3)

    def __define_beta_c_t_t0(self):
        """ function to define beta_c(t,t0) """
        self.beta_c_t_t0 = ((self.__t - self.__t0) / (self.beta_h + self.__t - self.__t0))**0.3

    def __define_phy_0(self):
        """ function to define phy_0 """
        self.phy_0 = self.phy_rh * self.beta_fcm * self.beta_fcm
    
    def __define_phy_t_t0(self):
        """ function to define phy(t,t0) """
        self.phy_t_t0 = self.phy_0 * self.beta_c_t_t0

    def calculation_note_fr(self, name, kind="WORD"):
        """ function to generate a calculation note """
        pass

# GET
    @property
    def t(self):
        return self.__t
    @property
    def t0(self):
        return self.__t0

# SET
    @t.setter
    def t(self, var):
        self.__t = var
        self.__define_value()
    @t0.setter
    def t0(self, var):
        self.__t0 = var
        self.__define_value()

if __name__ == "__main__":
    """
        Test 1:
            parameter: 
                fck = 30
                t = 18 000
                t0 = 50
                Ac = 11.33
                u = 33.39
                RH = 70
        
            result:
            beta_fcm = ~2.72531987
            beta_ t0 = ~0.4373067914
            h0 = ~678.6463012
            beta_rh = 
    """
    test = Creep(30, 18000, 50,11.33,39.5,70)

    print("h0: ",test.h0)
    print("beta_t0: ",test.beta_t0)
    print("beta_h: ",test.beta_h)
    print("phy_rh: ",test.phy_rh)
    print("phy_0: ",test.phy_0)
    print("phy_t_t0: ",test.phy_t_t0) 
 
