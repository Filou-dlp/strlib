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

class Deformation:
    """ 
    """

    def __init__(self, meds, beta, f_c, f_h, cross_section=0, mat_concrete=0, **kwargs):
        """ """
        self.__m = meds
        if beta == "ST":
            self.beta = 1
        elif beta == "LT":
            self.beta = 0.5
        self.__f_c = f_c
        self.__f_h = f_h
        if not bool(kwargs):
            self.__ih = cross_section.ih
            self.__fctm = mat_concrete.fctm
            self.__h = cross_section.h
            self.__xh = cross_section.xh
        else:
            for key, value in kwargs.items():
                if key == "ih":
                    self.__ih = value
                elif key == "fctm":
                    self.__fctm = value
                elif key == "h":
                    self.__h = value
                elif key == "xh":
                    self.__xh = value

        self.__define_value()
    
    def __define_value(self):
        """ """
        self.__define_mcr()
        self.__define_xi()
        self.__define_f_ec2()

    def __define_mcr(self):
        """ """
        self.mcr = self.__ih * self.__fctm / (self.__h \
                - self.__xh)

    def __define_xi(self):
        """ """
        self.xi = 1 - self.beta * (self.mcr / self.__m)**(1/2)
    
    def __define_f_ec2(self):
        """ """
        self.f_ec2 = self.xi * self.__f_c +  (1 - self.xi) * self.__f_h

if __name__ == "__main__":
    meds = 1
    beta = "ST"
    fc = 1
    fh = 1
    ih = 2
    xh = 1
    fctm = 3.5
    h = 3
    deform = Deformation(meds,  beta,  fc,  fh,  ih=ih, xh=xh,  fctm=fctm,  h=h)

    print("FEC2 : ",deform.f_ec2)
    print("xi : ",deform.xi)
    print("Mcr : ",deform.mcr)
    print("beta : ",deform.beta)