 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to make all calculation about beam (no matter matérial
"""
import sys
import math

from sollicitation.simple_flexion_uls import SimpleFlexureULS
# from sollicitation.simple_flexion_sls import SimpleFlexureSLS
from sollicitation.shear import Shear
from sollicitation.stress_verif import StressVerification
# from verification.shinkrage import Shinkrage
# from verification.creep import Creep
from verification.cracking import Cracking
from verification.cover import Cover



sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
# import TWord 


class PoutreRCStd:
    """
        Docstring
    """

    def __init__(self, load_edu, load_eds, cross_section, mat_concrete, \
            mat_steel, kind):
        """
            Constructor
            :@param load:
            :@param cross_section:
            :@param material:
            :@param kind:
            :@type load: tuple, double
            :@type cross_section: Section object
            :@type material: tuple, Material object
            :@type kind: string

        """
        # Variable that will be used
        self.__section_kind = kind
        self.__nedu = load_edu(0)
        self.__vedu = load_edu(1)
        self.__medu = load_edu(2)
        dict_edu = {"NED": self.__nedu, "VED": self.__vedu, \
                "MED": self.__medu}
        self.__neds = load_eds(0)
        self.__veds = load_eds(1)
        self.__meds = load_eds(2)
        
        self.__section = cross_section
        self.__mat_concete = mat_concrete
        self.__mat_steel = mat_steel     

        self.shear = Shear(dict_edu, self.__section, self.__mat_steel,\
                self.__mat_concete)
        self.flexion_uls = SimpleFlexureULS(self.__medu, \
                self.__section, self.__mat_steel, self.__mat_concete)

        self.stress_verif = StressVerification(self.__meds, self.__section)
        self.cracking = Cracking(self.__section, self.__mat_steel,\
                self.__mat_concete)
        self.cover = Cover(self.__section, self.__mat_concete)

        # Variable that will be used

    def make_calulation(self):
        """ function to make all calculation for a std beam """
        
        
if __name__ == "__main__":
    pass
