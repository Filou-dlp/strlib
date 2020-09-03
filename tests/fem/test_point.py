
import sys
sys.path.append(sys.path[0]+'/../../../strlib')

from strlib.fem.stiffness_calc import Point


class TestPoint:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        Point.reset()
        cls.test = Point(0, 0, "bou")
        cls.test2 = Point(1, 1)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
        del cls.test
        del cls.test2

    def test_get_Name_test_1(self):
        """ """
        assert self.test.name == "bou"

    def test_get_Name_test_2(self):
        """ """
        assert self.test2.name == "P2"

    def test_get_hyper_degree_bool(self):
        """ """
        self.test.define_support_condition(True, True, True)
        assert self.test.hyper_degree == 3
