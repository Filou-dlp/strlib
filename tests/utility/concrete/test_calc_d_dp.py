
import sys
sys.path.append(sys.path[0]+'/../../../strlib')
from utility.concrete.calc_d_dp import CalcDDp

class TestCalcDDp:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        h = 1000
        ast = (16, 16, 16, 16)
        c_nom = 40
        phy_t = 8
        ev = 30
        asc = (16, 18, 18, 18)
        cls.test = CalcDDp(h, ast, c_nom, phy_t, ev, asc=asc)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)

    def test_get_zg_ast(self):
        """ """
        assert self.test.zg_ast == 95
    
    def test_get_d(self):
        """ """
        assert self.test.d == 905
    
    def test_get_zg_asc(self):
        """ """
        assert self.test.zg_asc == 101.49723756906077

    def test_get_d_p(self):
        """ """
        assert self.test.d_p == 101.49723756906077