#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module docstring
"""

class SlabRC:
    """

    """
    def __init__(self, lx, ly, unit):
        """ construcor """
        if unit == "m":
            self.__unit = 100 # cm into m
        elif unit == "dm":
            self.__unit = 10 # cm into dm
        elif unit == "cm":
            self.__unit = 1 # cm into cm
        elif unit == "mm":
            self.__unit = 0.1 # cm into mm
        self.__lx = lx * self.__unit
        self.__ly = ly * self.__unit
        self.alpha = lx / ly
    
    def flexion(self):
        """ """
        if self.alpha <= 0.4:
            h = self.__lx / 30
        else:
            h = self.__lx / 40
        return h 

    def accoustic(self):
        """ """
        h = 14 / self.__unit
        return h
    
    def fire_safty(self, sf=1):
        """ """
        if sf == 0.5:
            h = 6 / self.__unit
        elif sf == 1:
            h = 7 / self.__unit
        elif sf == 1.5:
            h = 9 / self.__unit
        elif sf == 2:
            h = 11 / self.__unit
        elif sf == 3:
            h = 15 / self.__unit
        elif sf == 4:
            h = 17.5 / self.__unit
        return h

    def resistance(self, pu):
        """ 
            for μ = Mu / (b * d**2 * fcd)
            with fck = 25 MPa

            :@param pu: load in kN/m
        """

        lx = self.__lx / 100
        mu = pu * lx**2 / (10 * (1  + 2 * self.alpha**3))

        d = (3 * mu)**(1/2) 
        h = d + 3 / self.__unit
        return h 

if __name__ == "__main__":
    """ 
    
    """
    test = SlabRC(3.25, 6.00, "m")
    sf = 2
    G = 25
    Q = 10

    print("h flexion: ",  test.flexion())
    print("h accoustique: ",  test.accoustic())
    print("h securité au feu: ",  test.fire_safty(sf))
    h_min = max(test.flexion(), test.accoustic(), test.fire_safty(sf))
    pu = 1.35 * G * h_min / 100 + 1.5 * Q
    print("h min:", h_min)
    print("h resistance: ",  test.resistance(pu))