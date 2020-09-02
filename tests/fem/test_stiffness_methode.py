
import sys
from numpy import sum as npsum
sys.path.append(sys.path[0]+'/../../../strlib')

from strlib.fem.stiffness_calc import Point, Barre, Split, StiffnessMethode

class TestStiffnessMethode:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        Point.reset()
        Barre.reset()
        cls.P1 = Point(0, 0)
        P2 = Point(0, 1)
        cls.P3 = Point(1, 1)
        P4 = Point(2, 1)
        cls.P5 = Point(2, 0)

        cls.P1.define_support_condition(True, True, False)
        cls.P3.define_external_force(0, -10, 0)
        cls.P5.define_support_condition(True, True, False)

        B1 = Barre(cls.P1, P2)
        B2 = Barre(P2, cls.P3)
        B3 = Barre(cls.P3, P4)
        B4 = Barre(P4, cls.P5)

        cls.point = (cls.P1, P2, cls.P3, P4, cls.P5)
        barre = (B1, B2, B3, B4)

        cls.rslt = StiffnessMethode(cls.point, barre)

        del P2
        del P4
        del B1, B2, B3, B4

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
        del cls.rslt
        del cls.P1
        del cls.P3
        del cls.P5

    def test_support_tab(self):
        """ """
        rslt = npsum(self.rslt.support_tab)
        assert rslt == 4

    def test_d_tab(self):
        """ """
        rslt = npsum(self.rslt.d_tab)
        assert rslt == 11

    def test_force_tab(self):
        """ """
        rslt = npsum(self.rslt.force_tab)
        assert rslt == -10

    def test_connection_tab(self):
        """ """
        rslt = npsum(self.rslt.connect_tab)
        assert rslt == 8

    def test_intern_force(self):
        """ """
        rslt = self.P3.moment
        assert rslt == -3.9285714285714377

    def test_support_reaction(self):
        """ """
        rya = self.P1.ry
        ryb = self.P5.ry

        assert rya == ryb

    def test_test_iso(self):
        """ """
        assert StiffnessMethode.test_iso(self.point) == "Hyperstatic"
