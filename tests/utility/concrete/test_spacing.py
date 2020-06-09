
import sys
sys.path.append(sys.path[0]+'/../../../strlib')
from utility.concrete.spacing import Spacing

class TestSpacing:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        h = 400
        cnom = 35
        phy_t = 8
        phy_l = (25, 25, 25, 25, 25)
        dg = 5
        cls.test = Spacing(h, cnom, phy_t, phy_l, dg)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)

    def test_get_eh(self):
        """ """
        assert self.test.eh == 67.25
    
    def test_get_ev(self):
        """ """
        print("NotImplementedError")
        pass
    
    def test_get_eh_min(self):
        """ """
        assert self.test.eh_min == 25