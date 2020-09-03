
import sys
from unittest import mock
sys.path.append(sys.path[0]+'/../../../strlib')

from strlib.fem.stiffness_calc import Point, Barre, Split, StiffnessMethode


class TestStiffnessCalc_1:
    """
        First test for the class
        the structure will be two support beam with a force in the middle
        step for the division 50
        accurenty 7 decimal
    """
    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        Point.reset()
        Barre.reset()
        P1 = Point(0,0)
        P2 = Point(1,0)
        P3 = Point(2,0)

        P1.define_support_condition(True, True, False)
        P3.define_support_condition(True, True, False)

        P2.define_external_force(0,-10,0)

        B1 = Barre(P1, P2)
        B2 = Barre(P2, P3)

        points = (P1, P2, P3)
        barres = (B1, B2)

        nb_devid = 50    

        for i, barre in enumerate(barres):
            if i == 0:
                my_eltm = Split(barre.p_beg, barre.p_end,
                                barre, nb_devid, points, barres)
                cls.point_global = my_eltm.Point
                cls.barre_global = my_eltm.Barre
            else:
                my_eltm = Split(barre.p_beg, barre.p_end,
                                barre, nb_devid, cls.point_global,
                                cls.barre_global)
                cls.point_global = my_eltm.Point
                cls.barre_global = my_eltm.Barre

        cls.rslt = StiffnessMethode(cls.point_global, cls.barre_global)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
        del cls.rslt
        del cls.point_global, cls.barre_global

    def test_hyper_degree(self):
        """ """
        assert self.rslt.test_iso(self.point_global) == "Hyperstatic"

    def test_hyper_degree(self):
        """ """
        assert self.rslt.test_iso(self.point_global) == "Hyperstatic"
    
    def test_support_reaction(self):
        """ """
        ry1 = round(self.point_global[0].ry, 7)
        ry2 = round(self.point_global[-1].ry, 7)
        assert ry1 == 5
        assert ry2 == 5

    def test_max_moment(self):
        """ Test the moment in L/2 must be -PL/4 
        """
        m_max = round(self.point_global[50].moment, 7)
        assert m_max == -5

    def test_moment_x(self):
        """ 
            Test the moment in L/4 must be -PL/8 
            Test the moment in 3L/4 must be -PL/8 
        """
        m_L_4 = round(self.point_global[25].moment, 7)
        m_3L_4 = round(self.point_global[75].moment, 7)
        assert m_L_4 == -2.5
        assert m_3L_4 == -2.5
