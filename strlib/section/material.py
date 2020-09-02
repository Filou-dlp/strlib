#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define all material that we could used

    UNITS USED:
        - m -> Metter
        - MN -> Mega Newton
        - MPa -> Mega Pascal
"""

import math

class Material:
    """
        Class to define basic property of material

        :@param E: Young modulus of the material
        :@param NU: Poisson coef of the material
        :@param ALPHA: Thermical dilatation coefficient of the material
        :@type E: double
        :@type NU: double
        :@type ALPHA: double
    """
    # Attribut

    E = None
    NU = None
    ALPHA = None

    def __init__(self, young_modulus=0, poisson_coef=0, thermical_dilatation=0):
        self.E = young_modulus
        self.NU = poisson_coef
        self.ALPHA = thermical_dilatation


class MatConcrete(Material):
    """
        Class to define Concrete property

        :@param NU: Poisson coef of the material
        :@param ALPHA: Thermical dilatation coefficient of the material
        :@param ALPHA_CC: coefficient to calculatre fcd EC2
        :@param GAMMA_C: concrete security coefficient EC2
        :@param LAMBDA_RC: Value to transforme diagram EC2
        :@param ETA_RC: Value to transforme diagram EC2
        :@type NU: double
        :@type ALPHA: double
        :@type ALPHA_CC: double
        :@type GAMMA_C: double
        :@type LAMBDA_RC: double
        :@type ETA_RC: double
    """
    # Attribut

    NU = 0.2 # poisson coef
    ALPHA = 12 * 10**(-6) # K^(-1)

    # Coef
    ALPHA_CC = 1
    ALPHA_CC_PL = 0.8
    ALPHA_CT_PL = 0.8
    GAMMA_C = 1.5
    LAMBDA_RC = 0.8
    ETA_RC = 1

    def __init__(self, fck):
        """
            Constructor

            :@param fck: resitance of the concrete
            :@type fck: double
        """
        # Variable that will be used
        self.fcd = None
        self.fctd = None
        self.fcm = None
        self.fctk_005 = None
        self.fctk_095 = None
        self.Ecm = None
        self.epsilon_c1 = None
        self.fctm = None
        self.epsilon_cu1 = None
        self.epsilon_c2 = None
        self.epsilon_cu2 = None
        self.n = None
        self.epsilon_c3 = None
        self.epsilon_c2 = None
        self.epsilon_cu3 = None

        Material.__init__(self, poisson_coef=self.NU, thermical_dilatation=self.ALPHA)
        self.__fck = fck
        self.__define_value()

    def __define_value(self):
        """ Function to define all value EC2 """
        self.fcm = self.__fck + 8
        self.Ecm = 22 * (self.fcm / 10)**.3
        self.epsilon_c1 = min(0.7 * self.fcm**0.31, 2.8)

        if self.__fck <= 50:
            self.fctm = 0.3 * self.__fck**(2/3)
            self.fctk_005 = self.fctm * 0.7
            self.fctk_095 = self.fctm * 1.3
            self.epsilon_cu1 = 3.5
            self.epsilon_c2 = 2
            self.epsilon_cu2 = 3.5
            self.n = 2
            self.epsilon_c3 = 1.75
            self.epsilon_cu3 = 3.5
        else:
            self.fctm = 2.12 * math.log(1 + (self.fcm / 10))
            self.fctk_005 = self.fctm * 0.7
            self.fctk_095 = self.fctm * 1.3
            self.epsilon_cu1 = 2.8 + 27 * ((98 - self.fcm) / 100)**4
            self.epsilon_c2 = 2 + 0.085 * (self.__fck - 50)**0.53
            self.epsilon_cu2 = 2.6 + 35 * ((90 - self.__fck) / 100)**4
            self.n = 1.4 + 23.4 * ((90 - self.__fck) / 100)**4
            self.epsilon_c3 = 1.75 + 0.55 * (self.__fck - 50) / 40
            self.epsilon_cu3 = 2.6 + 35 * ((90 - self.__fck) / 100)**4

        self.__define_fcd()
        self.__define_fctd()
        self.__define_fctd_pl()

    def __define_fcd(self):
        """ Function to define fcd """
        self.fcd = self.__fck * self.ALPHA_CC / self.GAMMA_C

    def __define_fctd(self):
        """ function to define fctd """
        self.fctd = None
    
    def __define_fctd_pl(self):
        """ function to define fctd """
        self.ftcd_pl = self.fctk_005 * self.ALPHA_CT_PL / self.GAMMA_C
# GET
    @property
    def fck(self):
        """ fck getter """
        return self.__fck
    @property
    def E(self):
        """ Ecm getter because E = Ecm """
        return self.Ecm

# SET
    @fck.setter
    def fck(self, val):
        """ Redefine all value if we change fck """
        self.___fck = val
        self.__define_value()
    @E.setter
    def E(self, val):
        """ Ecm getter because E = Ecm """
        self.Ecm = val


class MatSteel(Material):
    """
        Class to define steel material (different from steel reinforcement !)
        :@param E: Young modulus of the material
        :@param NU: Poisson coef of the material
        :@param ALPHA: Thermical dilatation coefficient of the material
        :@type E: double
        :@type NU: double
        :@type ALPHA: double
    """
    # Attribute
    E = 210000 # MPa
    NU = 0.3
    ALPHA = 12 * 10**(-6) # K^(-1)

    # Coef
#    GAMMA_MO = 1

    def __init__(self, fyk):
        """
            Constructor
            :@param fyk: resistance of the section
            :@type fyk: double
        """
        Material.__init__(self, self.E, self.NU, self.ALPHA)
        self._fyk = fyk


class MatReinforcment(MatSteel):
    """
        Class to define reinforcement property for concrete
        :@param E: Young modulus of the material
        :@param GAMMA_S: steel security coefficient EC2
        :@type E: double
        :@type GAMMA_S: double
    """
    # Attribut
    E = 200000

    # Coef
    GAMMA_S = 1.15

    def __init__(self, fyk, nuance):
        """
            Constructor
            :@param fyk: resistance of the section
            :@param nuance: type of reinforcement that we will used
            :@type fyk: double
            :@type nuance: str

            Possibility for nuance:
                - A
                - B
                - C
        """
        # Variable that will be used
        self.fyd = None
        self.k = None
        self.epsilon_uk = None
        self.epsilon_p = None

        MatSteel.__init__(self, fyk)

        self.__nuance = nuance

        self.__define_value()

    def __define_value(self):
        """ Function to define all value """
        self.__define_fyd()
        self.__define_k()
        self.__define_epsilon_uk()
        self.__define_epsilon_p()

    def __define_fyd(self):
        """ function to define fyd """
        self.fyd = self._fyk / self.GAMMA_S

    def __define_k(self):
        """
            Function to define k in function of the nuance
        """
        if self.__nuance == "A":
            self.k = 1.05
        elif self.nuance == "B":
            self.k = 1.08
        elif self.nuance == "C":
            self.k = 1.15

    def __define_epsilon_uk(self):
        """
            Function to define epsilon_uk
            the value is for one thousand (°/oo)
        """
        if self.__nuance == "A":
            self.epsilon_uk = 25
        elif self.__nuance == "B":
            self.epsilon_uk = 50
        elif self.__nuance == "C":
            self.epsilon_uk = 75

    def __define_epsilon_p(self):
        """ function to define epsilon p = fyd / Es """
        self.epsilon_p = self.fyd / self.E

# GET
    @property
    def fyk(self):
        """ fyk getter """
        return self._fyk
    @property
    def nuance(self):
        """ nuance getter """
        return self.__nuance

# SET
    @fyk.setter
    def fyk(self, val):
        """ Redefine fyd value if we change fyk """
        self._fyk = val
        self.__define_fyd()
    @nuance.setter
    def nuance(self, val):
        """ Redefine k and epsilon_uk value if we change nuance """
        self.__nuance = val
        self.__define_k()
        self.__define_epsilon_uk()


if __name__ == "__main__":
    a = MatConcrete(30)

    print(a.fck)
    print(a.fcm)

    a.fck = 40

    print(a.fck)
    print(a.fcm)
