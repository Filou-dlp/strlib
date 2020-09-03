
import sys
import random
sys.path.append(sys.path[0]+'/../../../strlib')

from strlib.fem.stiffness_calc import Point, Barre, Split

class TestSplit_1:
    """
        Test split for Y = 0
    """

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        Point.reset()
        Barre.reset()
        P1 = Point(0, 0)
        P2 = Point(1, 0)
        P3 = Point(2, 0)
        B1 = Barre(P1, P2)
        B2 = Barre(P2, P3)
        B1.uniforme_load(0, -10, 0)
        cls.point = (P1, P2, P3)
        cls.barre = (B1, B2)

        del P1, P2, P3, B1, B2

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
        del cls.point
        del cls.barre

    def test_devid_point_barre(self):
        """ """
        for i in range(1, 200):  # Test with 2 000 iteratio; no bug
            Point.NB_POINT = len(self.point)
            Barre.NB_BARRE = len(self.barre)
            step = i
            my_split = Split(self.point[0], self.point[1], self.barre[0], \
                step, self.point, self.barre)

            
            point = my_split.Point
            barre = my_split.Barre
            nb = random.randrange(0, len(barre)-1)

            assert len(point) == (step + 2)
            assert len(barre) == step + 1
            assert self.barre[0].fy is True
            assert barre[nb].fy is True
            assert point[0].name == "P1"
            assert point[-2].name == "P2", f"valeur de i: {i}"


class TestSplit_2:
    """
        Test split no matter the value of X or Y
    """