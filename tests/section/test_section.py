
import sys
sys.path.append(sys.path[0]+'/../../strlib')

from section.section import FullSection, Rect, TriangleRect, Triangle, Circle, Custom


class TestFullSection:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        
        points = ((-2.4, 1.4),
                  (-2.4, 0.2),
                  (-4.4, 0.2),
                  (-4.4, 0),
                  (4.4, 0),
                  (4.4, 0.2),
                  (2.4, 0.2),
                  (2.4, 1.4),
                  (2.0, 1.2),
                  (2, 0.2),
                  (-2.0, 0.2),
                  (-2.0, 1.2),
                  (2, 1.2),
                  (2.4, 1.4),
                  (-2.4, 1.4))
        cls.test = FullSection(points)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)

    def test_length(self):
        """ """
        rslt = None
        assert self.test.length == rslt

    def test_area(self):
        """ """
        rslt = None
        assert round(self.test.area, 2) == rslt

    def test_sox(self):
        """ """
        rslt = None
        assert round(self.test.sox, 2) == rslt

    def test_soy(self):
        """ """
        rslt = None
        assert round(self.test.soy, 2) == rslt

    def test_iox(self):
        """ """
        rslt = None
        assert round(self.test.iox, 2) == rslt

    def test_ioy(self):
        """ """
        rslt = None
        assert round(self.test.ioy, 2) == rslt

    def test_ioyz(self):
        """ """
        rslt = None
        assert round(self.test.ioxy, 2) == rslt

class TestRect:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        b = 0.30
        h = 0.50
        kind = "BA"
        cls.test = Rect(b, h, kind)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
    
    def test_value(self):
        """ """
        assert self.test.yg == 0.25
        assert self.test.zg == 0.15
        assert self.test.area == 0.15
        assert self.test.inertia_y == 3.125 * 10**-3
        assert self.test.inertia_z == 1.125 * 10**-3
        assert self.test.sy == 0.0225
        assert self.test.sz == 0.0375


class TestCustom:
    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        b = 0.30
        h = 0.50
        kind = "BA"
        cls.test = Rect(b, h, kind)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)