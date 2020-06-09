 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module docstring
"""
from math import pi

class CalcDDp:
    """
        Docstring
    """

    def __init__(self, h, ast, c_nom, phy_t, ev=0, asc=0):
        """
            Constructor
        """
        self.zg_ast = self.__define_zg(ast, c_nom, phy_t, ev)
        self.d = h - self.zg_ast
        if asc !=0:
            self.zg_asc = self.__define_zg(asc, c_nom, phy_t, ev)
            self.d_p = self.zg_asc

    def __define_z_steel(self, steel, c_nom, phy_t, ev):
        """ """
        if isinstance(steel, (int, float)):
            tmp = c_nom + phy_t + steel / 2
            self.__z = tmp
        else:
            self.__z = []
            counter = 0
            ev_tmp = 0
            for i in steel:
                if counter % 2 == 0 and counter != 0:
                    ev_tmp += ev
                tmp = c_nom + phy_t + sum(steel[:counter]) + i / 2 + ev_tmp
                self.__z.append(tmp)
                counter += 1

    def __define_zg(self, steel, c_nom, phy_t, ev):
        """ """
        self.__define_z_steel(steel, c_nom, phy_t, ev)
        sy = 0
        s = 0
        if isinstance(steel, (int, float)):
            area = self.calc_section(steel)
            sy += area * self.__z
            s += area 
        else:
            max_ = len(steel)
            for i in range(0, max_):
                area = self.calc_section(steel[i])
                sy += area * self.__z[i]
                s += area 

        zg = sy / s
        return zg

    @staticmethod
    def calc_section(phy):
        """ """
        return phy**2 * pi / 4

if __name__ == "__main__":
    ast = (16, 16, 16, 16)
    asc = (18, 20, 18, 20)
    test = CalcDDp(1000, ast, 40, 8, 30, asc=asc)

    zg_ast = test.zg_ast
    print("zg ast: ", zg_ast)
    zg_asc = test.zg_asc
    print("zg asc: ", zg_asc)
    d = test.d
    print("d: ", d)
    d_p = test.d_p
    print("d': ", d_p)
