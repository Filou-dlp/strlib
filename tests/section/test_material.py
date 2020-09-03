
import sys
sys.path.append(sys.path[0]+'/../../strlib')

from section.material import MatConcrete, MatReinforcment

class TestMatConcrete:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
    
    def test_verify_preperty_below_50(self):
        """ """
        fck = 30 # MPa
        self.test = MatConcrete(fck)
        assert self.test.fcm == 38
        assert round(self.test.fctm, 2) == 2.90
        assert round(self.test.fctk_005, 2) == 2.03
        assert round(self.test.fctk_095, 2) == 3.77
        assert round(self.test.Ecm, 2) == 32.84
        assert round(self.test.epsilon_c1, 2) == 2.16
        assert round(self.test.epsilon_cu1, 2) == 3.5
        assert round(self.test.epsilon_c2, 2) == 2
        assert round(self.test.epsilon_cu2, 2) == 3.5
        assert round(self.test.n, 2) == 2
        assert round(self.test.epsilon_c3, 2) == 1.75
        assert round(self.test.epsilon_cu3, 2) == 3.5
        assert round(self.test.fcd, 2) == 20
        assert round(self.test.ftcd_pl, 2) == 1.08

    def test_verify_preperty_above_50(self):
        """ """
        fck = 80 # MPa
        self.test = MatConcrete(fck)
        assert self.test.fcm == 88
        assert round(self.test.fctm, 2) == 4.84
        assert round(self.test.fctk_005, 2) == 3.39
        assert round(self.test.fctk_095, 2) == 6.29
        assert round(self.test.Ecm, 2) == 42.24
        assert round(self.test.epsilon_c1, 2) == 2.8
        assert round(self.test.epsilon_cu1, 2) == 2.8
        assert round(self.test.epsilon_c2, 2) == 2.52
        assert round(self.test.epsilon_cu2, 2) == 2.6
        assert round(self.test.n, 2) == 1.4
        assert round(self.test.epsilon_c3, 2) == 2.16
        assert round(self.test.epsilon_cu3, 2) == 2.6
        assert round(self.test.fcd, 2) == 53.33
        assert round(self.test.ftcd_pl, 2) == 1.81


class TestMatReinforcment:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)

    def test_verify_propery(self):
        """ """
        fyk = 500
        nuance = "B"
        test = MatReinforcment(fyk, nuance)
        assert round(test.fyd, 0) == 435
        assert test.k == 1.08
        assert test.epsilon_uk == 50
        assert round(test.epsilon_p, 6) * 1000 == 2.174