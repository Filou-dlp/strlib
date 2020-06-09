 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define the cover of concrete section
"""
import sys
import math

sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
# import TWord


class Cover:
    """
        Class to make all stress vérification
        the whole class is in milimeter !
        :@param DELTA_C_DEV:
        :@type DELTA_C_DEV: integer
    """
    DELTA_C_DEV = 10
    C_MIN_DUR_TABLE_BA = None
    C_MIN_DUR_TABLE_BP = None

    C_NOM_MIN_GROUND = 0
    DELTA_CDUR_GAMMA = 0
    DELTA_CDUR_ST = 0
    DELTA_CDUR_ADD = 0
    DELTA_PAREMENT = 0
    DELTA_ABRASION = 0

    def __init__(self, cross_section=0, mat_concrete=0, **kwargs):
        """
            Constructor

            :@param structural_class: structural class of the concrete
            :@param exposition_class: exposition class of the concrete
            :@param cross_section: section property
            :@param mat_concrete: concrepte property
            :@type structural_class: string
            :@type exposition_class: string
            :@type cross_section: TSection object
            :@type mat_concrete: TMaterial object
            :@param **kwarg: enter all parameter individually to have a standalon class
        """
        if not bool(kwargs):
            self.__phy_max = cross_section.phy_max
            self.__phy_dg = mat_concrete.phy_dg
            self.__str_class = cross_section.structural_class
            self.__expo_class = cross_section.exposition_class
        else:
            for key, value in kwargs.items():
                if key == "str_class":
                    self.__str_class = value
                elif key == "expo_class":
                    self.__expo_class = value
                elif key == "phy_max":
                    self.__phy_max = value
                elif key == "phy_dg":
                    self.__phy_dg = value
                elif key == "kind":
                    self.__kind = value

        self.__define_cmin_dur_table()
        self.__define_value()
    
    def __define_cmin_dur_table(self):
        """ function to define cmin_dur table """
        self.C_MIN_DUR_TABLE_BA = (("NONE", "X0", "XC1", "XC2/XC3", "XC4", "XD1/XS1", "XD2/XS2", "XD3/XS3"), \
                                    ("S1",   10,    10,      10,      15,     20,        25,         30), \
                                    ("S2",   10,    10,      15,      20,     25,        30,         35), \
                                    ("S3",   10,    10,      20,      25,     30,        35,         40), \
                                    ("S4",   10,    15,      25,      30,     35,        40,         45), \
                                    ("S5",   15,    20,      30,      35,     40,        45,         50), \
                                    ("S6",   20,    25,      35,      40,     45,        50,         55))
        self.C_MIN_DUR_TABLE_BP = (("NONE", "X0", "XC1", "XC2/XC3", "XC4", "XD1/XS1", "XD2/XS2", "XD3/XS3"), \
                                    ("S1",   10,    15,      20,      25,     30,        35,         40), \
                                    ("S2",   10,    15,      25,      30,     35,        40,         45), \
                                    ("S3",   10,    20,      30,      35,     40,        45,         50), \
                                    ("S4",   10,    25,      35,      40,     45,        50,         55), \
                                    ("S5",   15,    30,      40,      45,     50,        55,         60), \
                                    ("S6",   20,    35,      45,      50,     55,        60,         65))
    
    def __define_value(self):
        """ function to define all value """
        self.__define_cmin_dur()
        self.__define_cmin_b()
        self.__define_cmin()
        self.__define_cnom()

    def __define_cmin_dur(self):
        """ function to define cmin,dur """
        if self.__expo_class == "X0":
            col = 1
        elif self.__expo_class == "XC1":
            col = 2
        elif self.__expo_class == "XC2" or self.__expo_class == "XC3":
            col = 3
        elif self.__expo_class == "XC4":
            col = 4
        elif self.__expo_class == "XD1" or self.__expo_class == "XS1":
            col = 5
        elif self.__expo_class == "XD2" or self.__expo_class == "XS2":
            col = 6
        elif self.__expo_class == "XD3" or self.__expo_class == "XS3":
            col = 7
        
        row = int(self.__str_class[1:]) 
        if self.__kind == "BA":
            self.cmin_dur = self.C_MIN_DUR_TABLE_BA[row][col]
        elif self.__kind == "BP":
            self.cmin_dur = self.C_MIN_DUR_TABLE_BP[row][col]
        
    def __define_cmin_b(self):
            """ function to define cmin,b """
            dg = 0 if self.__phy_dg <= 32 else 5
            self.cmin_b = self.__phy_max + dg
                

    def __define_cmin(self):
        """ function to define cmin """
        self.cmin = max(self.cmin_b, self.cmin_dur + self.DELTA_CDUR_GAMMA - \
            self.DELTA_CDUR_ST - self.DELTA_CDUR_ADD, 10) + \
                self.DELTA_PAREMENT + self.DELTA_ABRASION
    
    def __define_cnom(self):
        """ function to define cnom """
        self.cnom = max(self.cmin + self.DELTA_C_DEV, self.C_NOM_MIN_GROUND)

    def calculation_note_fr(self, name, kind="WORD"):
        """ function to make calculation note about cover """
        pass

if __name__ == "__main__":
    test = Cover("S4", "XD3", phy_max=16, phy_dg=5, kind="BA")

    print(test.cmin_dur)
    print(test.cmin_b)
    print(test.cnom)