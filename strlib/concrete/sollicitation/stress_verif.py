 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to calculate stress in ELS
"""
import sys
sys.path.append(sys.path[0]+'/../../Office_lib')
print(sys.path)
# import TWord


class StressVerification:
    """
        Class to make all stress vérification
    """
    def __init__(self, meds, cross_section=0, **kwargs):
        """
            Constructor

            :@param Meds:
            :@param cross_section:
            :@param mat_steel:
            :@type Meds: double
            :@type cross_section: TSection object
            :@type mat_steel: TMaterial object
        """
        self.__m_eds = meds

        if not bool(kwargs):
            self.__section = cross_section
            self.__d = self.__section.d
            self.__d_p = self.__section.d_p
            self.__ih = self.__section.ih
            self.__xh = self.__section.xh
            self.__alpha_eq = self.__section.alpha_eq
        else:
            for key, value in kwargs.items():
                if key == "d":
                    self.__d = value
                if key == "Ih":
                    self.__ih = value
                if key == "xh":
                    self.__xh = value
                if key == "alpha_eq":
                    self.__alpha_eq = value

    def make_calculation(self):
        """ function to make all calculation """
        self.__define_sigma_c()
        self.__define_sigma_s()

    def __define_sigma_c(self):
        """ function to define sigma_c """
        self.sigma_c = self.__m_eds * \
                    self.__xh / self.__ih

    def __define_sigma_s(self):
        """ function to define sigma_s """
        self.sigma_s = self.__alpha_eq * self.__m_eds * \
                    (self.__d - self.__xh) / self.__ih

    @staticmethod
    def limite(fcy_k, kind="CARA"):
        """
            function to show the limite of the project

            ELU -> Not concidere
            ELS Cara:
                sigma_c = 0.6 * fck
                sigma_s = 0.8 * fyk

            ELS Freq:
                sigma_c = DON'T KNOW
                sigma_s = DON'T KNOW

            ELS QP:
                sigma_c = 0.45 * fck
                sigma_s = 0.32 * fyk - 0.52*fyk
        """
        if kind == "ELU":
            return ("INF", "INF") # sigma_c and sigma_s
        elif kind == "CARA":
            return (fcy_k[0] * 0.6, fcy_k[1] * 0.8) # sigma_c and sigma_s
        elif kind == "FREQ":
            return ("DON'T KNOW", "DON'T KNOW") # sigma_c and sigma_s
        elif kind == "QP":
            return (fcy_k[0] * 0.45, fcy_k[1] * 0.32) # sigma_c and sigma_s

    def calculation_note_fr(self, kind="WORD"):
        """ Function to make the calculation note """

if __name__ == "__main__":
    """ Test our program """
    test = StressVerification(d=1,Ih=2,xh=3,meds=1,alpha_eq=15)
    test.make_calculation()
    print(test.sigma_c)
    print(test.sigma_s)