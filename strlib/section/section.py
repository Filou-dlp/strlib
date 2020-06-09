#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to define the section for a project

    UNITS USED:
        - m -> Metter
        - MN -> Mega Newton
        - MPa -> Mega Pascal
"""

import math

from .section_material import ReinforcedConcrete as RC
from .section_material import Steel, Mixte, Timber

class FullSection: # Full section
    """
        Class for every section
    """

 # Attribute

    def __init__(self, point):
        """ Constructor """
        
        self.__Point = point
        
        self.__coords = []
        for i,ii in self.__Point:
            self.__X = i
            self.__Y = ii
            self.__coords.append((self.__X,self.__Y))
        self.__define_Area()   
        self.__define_Sox()
        self.__define_Soy()
        self.__define_Inertia_ox()
        self.__define_Inertia_oy()
        self.__define_Inertia_oyz()
    
    def __Length(self):
        pass
    
    def __define_Area(self): # Correct
        self.__Area = 0
        self.__Area_pt = []
        for count in range(len(self.__coords)-1):
            y = self.__coords[count][0] * self.__coords[count+1][1]
            x = self.__coords[count+1][0] * self.__coords[count][1]
            z = y - x
            self.__Area_pt.append(abs(z/2))
            self.__Area += z
        self.__Area = abs(self.__Area/2.0)

    def __define_Sox(self): # Correct
        self.__Sox = 0
        self.__Sox_pt = []
        for count in range(len(self.__coords)-1):
            z = self.__Area_pt[count]*(self.__coords[count][1]+self.__coords[count+1][1])/3
            self.__Sox_pt.append(z)
            self.__Sox += z  
        
    def __define_Soy(self): # Correct
        self.__Soy = 0
        self.__Soy_pt = []
        for count in range(len(self.__coords)-1):
            z = self.__Area_pt[count]*(self.__coords[count][0]+self.__coords[count+1][0])/3
            self.__Soy_pt.append(z)
            self.__Soy += z   

    def __define_Inertia_ox(self): # Correct
        self.__Iox = 0
        self.__Iox_pt = []
        for count in range(len(self.__coords)-1):
            y1 = self.__coords[count][1]
            y2 = self.__coords[count+1][1]
            z = self.__Area_pt[count]*(y1**2 + y1*y2 + y2**2)/6
            self.__Iox_pt = z
            self.__Iox += z

    def __define_Inertia_oy(self): # Correct
        self.__Ioy = 0
        self.__Ioy_pt = []
        for count in range(len(self.__coords)-1):
            x1 = self.__coords[count][0]
            x2 = self.__coords[count+1][0]
            z = self.__Area_pt[count]*(x1**2 + x1*x2 + x2**2)/6
            self.__Ioy_pt = z
            self.__Ioy += z

    def __define_Inertia_oyz(self): # Correct
        self.__Ioxy = 0
        self.__Ioxy_pt = []
        for count in range(len(self.__coords)-1):
            x1 = self.__coords[count][0]
            x2 = self.__coords[count+1][0]
            y1 = self.__coords[count][1]
            y2 = self.__coords[count+1][1] 
            z = self.__Area_pt[count]*(x1*y1 + y2*x2 + (x2*y1+x1*y2)/2)/6
            self.__Ioxy_pt = z
            self.__Ioxy += z
            
    def __define_Gravity_center(self):
        pass   
    def __define_Inertia_principal_y(self):
        pass
    def __define_Inertia_principal_y(self):
        pass
    def __define_Inertia_principal_yz(self):
        pass      
 # Set
    def __set_(self):
        pass

 # Get
    def __get_Area(self):
        return self.__Area
    def __get_Sox(self):
        return self.__Sox
    def __get_Soy(self):
        return self.__Soy
    def __get_Iox(self):
        return self.__Iox
    def __get_Ioy(self):
        return self.__Ioy
    def __get_Ioxy(self):
        return self.__Ioxy

    Area = property(__get_Area)
    Sox = property(__get_Sox)
    Soy = property(__get_Soy)
    Iox = property(__get_Iox)
    Ioy = property(__get_Ioy)
    Ioxy = property(__get_Ioxy)


class Rect(RC, Steel, Mixte, Timber):
    """
        Class to define a rectangular section
    """
    def __init__(self, b, h, kind):
        """
            Constructor
            :@param b: base of the section
            :@param h: heigth of the section
            :@param kind: type of material for special section properties
            :@type b: double
            :@type h: double
            :@type kind: string
        """
        # Variable that will be used
        self.yg = None
        self.zg = None
        self.area = None
        self.inertia_y = None
        self.inertia_z = None
        self.sy = None
        self.sz = None

        if kind == "BA":
            RC.__init__(self, h)
        elif kind == "ACIER":
            Steel.__init__(self)
        elif kind == "MIXTE":
            Mixte.__init__(self)
        elif kind == "TIMBER":
            Timber.__init__(self)

        self.__b = b
        self._h = h

        self.__define_value()

    def __define_value(self):
        """ Function to define all values """
        self.yg = self.__b / 2
        self.zg = self._h / 2
        self.area = self.__b * self._h
        self.inertia_y = self.__b * self._h**3 / 12
        self.inertia_z = self._h * self.__b**3 / 12
        self.sy = self.area * self.zg
        self.sz = self.area * self.yg
     
 # GET
    @property
    def b(self):
        """ b getter """
        return self.__b
    @property
    def h(self):
        """ h getter """
        return self._h

 # SET
    @b.setter
    def b(self,val):
        """ redefine value when change b """
        self.__b = val
        self.__define_value()
        self._define_value()
    @h.setter
    def h(self,val):
        """ redefine value when change h """
        self._h = val
        self.__define_value()
        self._define_value()


class TriangleRect:
    """
    """
    def __init__(self, b, h):
        self.__b = b
        self.__h = h
        
        self.__define_value()
    
    def __define_value(self):
        self.__Area = self.__b * self.__h/2
        self.__Yg = self.__h/3
        self.__Zg = self.__b/3
        self.__Sy = self.__Area * self.__Zg
        self.__Sz = self.__Area * self.__Yg
        self.__Inertia_y = self.__b*self.__h**3 /36
        self.__Inertia_z = self.__h*self.__b**3 /36

 # Set
    def __set_b(self,var):
        self.__b = var
        self.__define_value()
    def __set_h(self,var):
        self.__h = var
        self.__define_value()

 # Get
    def __get_b(self):
        return self.__b
    def __get_h(self):
        return self.__h
    def __get_Yg(self):
        return self.__Yg
    def __get_Zg(self):
        return __self.__Zg
    def __get_Sy(self):
        return self.__Sy
    def __get_Sz(self):
        return self.__Sz
    def __get_Area(self):
        return self.__Area
    def __get_Inertia_y(self):
        return self.__Inertia_y
    def __get_Inertia_z(self):
        return self.__Inertia_z
    
    b = property(__get_b,__set_b)
    h = property(__get_h, __set_h)
    Yg = property(__get_Yg)
    Zg = property(__get_Zg)
    Sy = property(__get_Sy)
    Sz = property(__get_Sz)
    Area = property(__get_Area)
    Inertia_y = property(__get_Inertia_y)
    Inertia_z = property(__get_Inertia_z)


class Triangle:
    """
    """
    def __init__(self, b, h):
        self.__Area = b * h /2
        self.__Inertia_y = b*h**3 /36
        self.__Inertia_z = h*b**3 /36


class Circle:
    """
    """
    PI = math.pi
    
    def __init__(self, r):
        self.__Area = self.__PI * r**2


class Custom:
    """
    """
    def __init__(self, Area=0,Inertia_y=0,Inertia_z=0):
        self.area = 0
        self.inertia_y = 0
        self.inertia_z = 0
        
        self.define_value()

    def define_value(self):
        self.roh = 0
        self.v = 0
        self.v_prime = 0
        self.sy = 0
        self.sz = 0
        self.h = 0


if __name__ == "__main__":
    P1 = (0,0)
    P2 = (2,0)
    P3 = (1,1)
    P4 = (0,1)
    
    point = (P1,P2,P3,P4)
    a = FullSection(point)
    
    print(a.Area)
    print(a.Sox)
    print(a.Soy)
    print(a.Iox)
    print(a.Ioy)
    print(a.Ioxy)
