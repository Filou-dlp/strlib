#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define section variable specific to a material

    UNITS USED:
        - m -> Metter
        - MN -> Mega Newton
        - MPa -> Mega Pascal
"""

class ReinforcedConcrete:
    """
        Class to define default variable for concrete section
    """
    ALPHA_SHEAR = 90

    def __init__(self, h):
        """
            Constructor
        """
        # Variable that will be used
        # Steel or prestress
        self.ast = None
        self.asc = None
        self.asp = None # Prestress reinforce

        self.astc = None # ast + asc

        self.phy_t_max = None # Maximal size of a reinforcement

        self._steel_kind = "HA" # type of steel, by default HA

        # Equivalent coefficient
        self._alpha_eq = 15 # Defautl value for RC
        # Geometrical property
        self._Ih = None # homogenous inertia
        self._Ic = None # Crack inertia
        
        self._xh = None # Homogenous neutral axis
        self._xc = None # Crack neutral axis
        self._xn = None # Neutral axis
        
        self._d = None
        self._d_p = None

        self._h = h

        # Space
        self._ev = None # Vertical space between two reinforcement
        self._eh = None # Horizontal space between two reinforcement

        # Concrete cover
        self._cnom = None

        # Exposition class
        self._expo_class = None

        # Structural class
        self._str_class = None

        self._define_value()
    
    def _define_value(self):
        """ function to define value """
        self.__define_d()
        self.__define_d_p()

    def __define_d(self):
        """ function to define d """
        self._d = 0.9 * self._h

    def __define_d_p(self):
        """ function to define d """
        self._d_p = 0.1 * self._h

    def __define_steel_kind(self):
        """
            function to define steel kind
            value could be:
                - HA
                - PC -> prestress concrete
                - RL -> Ronds lisse
        """
        self._steel_kind = "HA"
    # GET
    @property
    def d(self):
        """ d getter """
        return self._d
    @property
    def d_p(self):
        """ d_p getter """
        return self._d_p
    @property
    def steel_kind(self):
        return self._steel_kind

    # SET
    @d.setter
    def d(self, val):
        """ redefine value when changing d """
        self._d = val
        self._define_value()

    @d_p.setter
    def d_p(self, val):
        """ redefinie value when changing d_p """
        self._d_p = val
        self._define_value()

    @steel_kind.setter
    def steel_kind(self, val):
        self._steel_kind = val
        self.__define_steel_kind()


class Steel:

    def __init__(self):
        pass


class Mixte:
    
    def __init__(self):
        pass
        

class Timber:
    
    def __init__(self):
        pass

if __name__ == "__main__":
    pass