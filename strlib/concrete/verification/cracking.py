 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module docstring
"""
import sys
import math

sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
import TWord

class Cracking:
    """
        Class to calcul cracking
    """

    def __init__(self, cross_section=0, mat_concrete=0, mat_steel=0, **kwargs):
        """
            Construtor
            :@param cross_section: Section property
            :@param mat_concrete: Concrete property
            :@param mat_steel: Steel reinforcement property
            :@param **kwargs: parameter to make the application standalone
            :@type cross_section: Setion object
            :@type mat_concrete: Material object
            :@type mat_steel: Material object
        """
        self.__section = cross_section
        self.__mat_concrete = mat_concrete
        self.__mat_steel = mat_steel

        # Variable that will be used

        # Asmin
        self.as_min = None

    def make_calcultation(self):
        """ Function to make calculation """
        self.__define_sr_max()
        self.__define_esm_ecm()
        self.__define_wk()
        self.__define_as_min()

    def __define_sr_max(self:)
        """ function to define sr_max """
        if self.__section.eh > 5 * (self.__section.cnom + self.__section.phy_t_max / 2):
            self.sr_max = 1.3 * (self.__section.h - self.__section.xn)
        else:
            if self.__section.cnom <= 0.025: # 25 mm -> 0.025 m
                k3 = 3.4
            else:
                k3 = 3.4 * ((25 / self.__section.cnom)**2)**(1/3)
            
            if self.__section.steel_kind == "HA":
                k1 = 0.8
            else:
                k1 = 1.6
            
            if self.__calc_type == "FLEX":
                k2 = 0.5
            elif self.__calc_type == "TRACT PUR":
                k2 = 1
            else:
                epsilon_1 = ???
                epsilon_2 = ???

                k2 = (epsilon_1 + epsilon_2) / (2 * max(epsilon_1, epsilon_2))

            k4 = 0.425 # A.N.
            
            self.sr_max = k3 * self.__section.cnom + k1 * k2 * k4 * self.__section.phy_max / self.__roh_p_eff 
            

    def __define_esm_ecm(self, time="LONG"):
        """ function to define epsilon_sm - epsilon_cm """
        Es = self.__mat_steel.E
        fct_eff = self.__mat_concrete.fctm
        kt = 0.4 if time == "LONG" else 0.6

        hc_eff = min(2.5 * (self.__section.h - self.__section.d),\
                (self.__section.h - self.__section.xn) / 3,\
                self.__section.h / 2)
        Ac_eff = self.__section.b * hc_eff
        self.__roh_p_eff = self.__section.astc + xi_prc * self.__section.ap / Ac_eff
        
        self.esm_ecm = max(sigma_s - kt * fct_eff / self.__roh_p_eff * (1 + self.__section.alpha_eq * roh_p_eff) / Es, 0.6 * simga_s / Es)

    def __define_wk(self):
        """ function to define wk """
        self.wk = self.sr_max * self.esm_ecm

    def __define_as_min(self):
        """ """
        sigma_s = self.__mat_steel.fyk
        self.as_min = kc * k * fct_eff * self.__section.area / sigma_s


if __name__ == "__main__":
    pass
