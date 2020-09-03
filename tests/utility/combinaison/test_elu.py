import sys
sys.path.append(sys.path[0]+'/../../strlib')
from utility.combinaison.elu import Combinaison as comb


class TestCombinaisons:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
    
    def test_ulu_equ_g_favorable(self):
        """ """
        g = 20
        q = 100
        s = 50
        coef_q = (0, 0.7, 1.5)
        coef_s =  (0, 0.75, 1.5)
        rslt = comb.ulu_equ_g_favorable(g, q, s, coef_q, coef_s)
        tmp = (23.0, 60.5, 98.0, 93.0, 168.0, 173.0, 210.5)
        assert rslt == tmp

    # def test_ulu_equ_g_defavorable(self):
    #     """ """
    #     pass
