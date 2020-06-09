 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to calculate the inertia
"""
import sys
import math

class IntertiaRect:
    """
        Docstring
    """

    def __init__(self, b, h, alpha_eq, d, ast, d_p, asc):
        """
            Constructor
        """
        self.__b = b
        self.__h = h
        self.__alpha_eq = alpha_eq
        self.__d = d
        self.__ast = ast
        self.__d_p = d_p
        self.__asc = asc
        # variable that will be used
        self.x_crack = None
        self.inertia_crack = None
        self.x_homogenous = None
        self.inertia_homogenous = None

    def make_calculation(self):
        """ """
        self.__define_neutral_axe_homogenous()
        self.__define_neutral_axe_crack()
        self.__define_inertie_homogenous()
        self.__define_inertie__crack()

    def __define_neutral_axe_homogenous(self):
        """ """
        first = self.__b * self.__h**2 / 2
        second = self.__alpha_eq * (self.__d * self.__ast + \
                self.__d_p * self.__asc)
        third = self.__b * self.__h + self.__alpha_eq * (self.__ast + self.__asc)

        self.x_homogenous = (first + second) / third

    def __define_inertie_homogenous(self):
        """ """
        first = self.__b * self.__h**3 / 12 + self.__b * self.__h * \
                (self.x_homogenous - self.__h / 2)**2
        second = self.__alpha_eq * self.__asc * \
                (self.x_homogenous - self.__d_p)**2
        third = self.__alpha_eq * self.__ast * \
                (self.x_homogenous - self.__d)**2

        self.inertia_homogenous = first + second + third

    def __define_neutral_axe_crack(self):
        """ """
        first = - self.__alpha_eq * (self.__asc + self.__ast)
        second = self.__alpha_eq**2 * (self.__asc + self.__ast)**2
        third = 2 * self.__b * self.__alpha_eq * (self.__asc * self.__d_p + \
                self.__ast * self.__d)
        self.x_crack = (first + (second + third)**(1/2)) / self.__b

    def __define_inertie__crack(self):
        """ """ 
        first = self.__b  * self.x_crack**3 / 3
        second = self.__alpha_eq * self.__asc * (self.x_crack - self.__d_p)**2
        third = self.__alpha_eq * self.__ast * (self.x_crack - self.__d)**2
        
        self.inertia_crack = first + second + third


class IntertiaTRect:
    """
        Docstring
    """

    def __init__(self, bw, beff, h, hf, alpha_eq, d, ast, d_p, asc):
        """
            Constructor
        """
        self.__bw = bw
        self.__beff = beff
        self.__h = h
        self.__hf = hf
        self.__alpha_eq = alpha_eq
        self.__d = d
        self.__ast = ast
        self.__d_p = d_p
        self.__asc = asc
        # variable that will be used
        self.x_crack = None
        self.inertia_crack = None
        self.x_homogenous = None
        self.inertia_homogenous = None

    def make_calculation(self):
        """ """
        self.__define_neutral_axe_homogenous()
        self.__define_inertie_homogenous()

        self.__define_neutral_axe_crack_inside()
        if self.x_crack > self.__hf:
            self.__define_neutral_axe_crack_outside()
            self.__define_inertie_crack_outside()
        else:
            self.__define_inertie_crack_inside()

    def __define_neutral_axe_homogenous(self):
        """ """
        first = self.__bw * self.__h**2 / 2 + (self.__beff - self.__bw) / 2 * \
                self.__hf**2
        second = self.__alpha_eq * (self.__d * self.__ast + \
                self.__d_p * self.__asc)
        third = (self.__beff - self.__bw) * self.__hf + self.__bw * self.__h + \
                self.__alpha_eq * (self.__ast + self.__asc)

        self.x_homogenous = (first + second) / third

    def __define_inertie_homogenous(self):
        """ """
        first = self.__beff * self.x_homogenous**3 /3
        second = - (self.__beff - self.__bw) * (self.x_homogenous - \
                self.__hf)**3 /3 + (self.__h - self.x_homogenous)**3 / 3
        third = self.__alpha_eq * self.__ast * (self.__d - \
                self.x_homogenous)**2 + self.__alpha_eq * \
                self.__asc * (self.__d_p - self.x_homogenous)**2

        self.inertia_homogenous = first + second + third

    def __define_neutral_axe_crack_inside(self): # A vérifier
        """ """
        first = - self.__alpha_eq * (self.__ast + self.__asc)
        second = self.__alpha_eq**2 * (self.__ast + self.__asc)**2
        third = self.__alpha_eq * self.__beff * (self.__ast * self.__d + \
                self.__asc * self.__d_p)
        self.x_crack = (first + (second + third)**(1/2)) / self.__beff

    def __define_inertie_crack_inside(self): # A vérifier
        """ """ 
        first = self.__beff * self.x_crack / 3
        second = self.__alpha_eq * self.__ast * (self.__d - self.x_crack)**2
        third = self.__alpha_eq * self.__asc * (self.__d_p - self.x_crack)**2
        
        self.inertia_crack = first + second + third

    def __define_neutral_axe_crack_outside(self):
        """ """
        first = -((self.__beff - self.__bw) * self.__hf + self.__alpha_eq * \
                (self.__ast + self.__asc))
        second = ((self.__beff - self.__bw) * self.__hf + self.__alpha_eq * \
                (self.__ast + self.__asc))**2
        third = 2 * self.__bw * (self.__beff * self.__bw) / 2 * self.__hf **2
        fourth = self.__alpha_eq * (self.__asc * self.__d_p + \
                self.__ast * self.__d)
        self.x_crack = (first + (second + third + fourth)**(1/2)) / self.__bw
    
    def __define_inertie_crack_outside(self):
        """ """
        first = self.__bw * self.x_crack**3 / 3 + (self.__beff - self.__bw) * \
                self.__hf**3 / 12
        second = (self.__beff - self.__bw) * self.__hf * \
                (self.x_crack - self.__hf / 2)**2
        third = self.__alpha_eq * self.__ast * (self.x_crack - self.__d)**2 + \
                self.__alpha_eq * self.__asc * (self.x_crack - self.__d_p)**2
        self.inertia_crack = first + second + third

if __name__ == "__main__":
    pass
