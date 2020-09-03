
import sys
from numpy import sum as npsum
from unittest import mock
sys.path.append(sys.path[0]+'/../../../strlib')

from strlib.fem.stiffness_calc import Point, Barre


class TestBarreWithoutMatSec:

    @classmethod
    def setup_class(cls):
        print("\nAvant mon teste unitaire\n") # pytest -s
        Point.reset()
        P1 = Point(0, 0)
        P2 = Point(1, 1)
        cls.__length = 2**0.5
        cls.test = Barre(P1, P2)

        del P1
        del P2

    @classmethod
    def teardown_class(cls):
        print("\naprès mon test unitaire")

    def test_get_length(self):
        """ """
        assert self.test.length == self.__length

    def test_get_alpha(self):
        """ """
        assert self.test.angle == 45

    def test_get_rot_mat(self):
        """ """
        tmp = npsum(self.test.rot_mat)
        rslt = 2 + 2 * 2**0.5
        assert tmp == rslt

    def test_get_k_local_fixed_fixed(self):
        """ """
        self.test.define_local_mat("FIXED", "FIXED")
        tmp = round(npsum(self.test.k_local), 13)
        rslt = 8.4852813742386
        
        assert tmp == rslt

    def test_get_k_local_pined_fixed(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_fixed_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_pined_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "PINED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_lintel_linted(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("LINTEL", "LINTEL")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_barre(self):
        """ """
        tmp = round(npsum(self.test.k_barre), 14)
        rslt = 8.48528137423857
        assert tmp == rslt

    def test_uniform_load_fy_global_0(self):
        """ """
        py = -10
        self.test.uniforme_load(0, py, 0, "GLOBAL", 0)
        fx = 0
        fy = py * self.__length / 2
        mz = py * self.__length**2 / 12
        assert self.test.fy_x_beg == fx
        assert self.test.fy_y_beg == fy
        assert self.test.fy_m_beg == mz
        assert self.test.fy_x_end == fx
        assert self.test.fy_y_end == fy
        assert self.test.fy_m_end == -mz

    def test_uniform_load_fy_global_45(self):  # NotImplentedYet
        """ """
        py = -10
        angle = 45
        self.test.uniforme_load(0, py, 0, "GLOBAL", angle)
        fx = None
        fy = None
        mz = None
        # assert self.test.Fy_x_beg == fx
        # assert self.test.Fy_y_beg == fy
        # assert self.test.Fy_m_beg == mz
        # assert self.test.Fy_x_end == fx
        # assert self.test.Fy_y_end == fy
        # assert self.test.Fy_m_end == -mz

    def test_temperature_dt_x(self):
        """ """
        dt_x = 12  # °
        self.test.temperature(dt_x, 0)
        fx = dt_x / self.__length
        fy = 0
        mz = 0
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_temperature_dt_m(self):
        """ """
        dt_m = 12  # °
        self.test.temperature(0, dt_m)
        fx = 0
        fy = 0
        mz = dt_m
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_prestress_load(self): # NotImplentedYet
        """ """
        pass
         # NotimplementedYet


class TestBarreWithMatSec:

    @classmethod
    def setup_class(cls):
        # print("Avant mon teste unitaire", cls) # pytest -s
        P1 = Point(0, 0)
        P2 = Point(45, 49)
        cls.__length = (45**2 + 49**2)**0.5
        cls.__mat = mock
        cls.__mat.E = 35000
        cls.__mat.alpha = 10 * 10**(-6)
        cls.__section = mock
        cls.__section.area = 11.33
        cls.__section.inertia_y = 25.5375
        cls.__section.h = 4.2
        cls.test = Barre(P1, P2, cls.__section, cls.__mat)
        del P1, P2

    @classmethod
    def teardown_class(cls):
        pass #print("après mon test unitaire", cls)
        del cls.test
        del cls.__length, cls.__mat, cls.__section

    def test_get_length(self):
        """ """
        assert self.test.length == self.__length

    def test_get_alpha(self):
        """ """
        assert self.test.angle == 47.43664824681013

    def test_get_rot_mat(self):
        """ """
        tmp = npsum(self.test.rot_mat)
        rslt = 4.705619998306716
        assert tmp == rslt

    def test_get_k_local_fixed_fixed(self):
        """ """
        self.test.define_local_mat("FIXED", "FIXED")
        tmp = npsum(self.test.k_local)
        rslt = 161221.13164910144
        assert tmp == rslt

    def test_get_k_local_pined_fixed(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_fixed_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_pined_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "PINED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_lintel_linted(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("LINTEL", "LINTEL")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_barre(self):
        """ """
        tmp = npsum(self.test.k_barre)
        rslt = 161221.13164910147
        assert tmp == rslt

    def test_uniform_load_fy_global_0(self):
        """ """
        py = -10
        self.test.uniforme_load(0, py, 0, "GLOBAL", 0)
        fx = 0
        fy = py * self.__length / 2
        mz = py * self.__length**2 / 12
        assert self.test.fy_x_beg == fx
        assert self.test.fy_y_beg == fy
        assert self.test.fy_m_beg == mz
        assert self.test.fy_x_end == fx
        assert self.test.fy_y_end == fy
        assert self.test.fy_m_end == -mz

    def test_uniform_load_fy_global_45(self):  # NotImplentedYet
        """ """
        py = -10
        angle = 45
        self.test.uniforme_load(0, py, 0, "GLOBAL", angle)
        fx = None
        fy = None
        mz = None
        # assert self.test.Fy_x_beg == fx
        # assert self.test.Fy_y_beg == fy
        # assert self.test.Fy_m_beg == mz
        # assert self.test.Fy_x_end == fx
        # assert self.test.Fy_y_end == fy
        # assert self.test.Fy_m_end == -mz

    def test_temperature_dt_x(self):
        """ """
        dt_x = 12  # °
        self.test.temperature(dt_x, 0)
        fx = self.__section.area * self.__mat.E * self.__mat.alpha * \
            dt_x / self.__length
        fy = 0
        mz = 0
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_temperature_dt_m(self): 
        """ """
        dt_m = 12  # °
        self.test.temperature(0, dt_m)
        fx = 0
        fy = 0
        mz = self.__section.inertia_y * self.__mat.E * self.__mat.alpha * \
            dt_m / self.__section.h
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_prestress_load(self):  # NotImplentedYet
        """ """
        pass
         # NotimplementedYet


class TestBarreWithMatSecRedifine:

    @classmethod
    def setup_class(cls):
        # print("Avant mon teste unitaire", cls) # pytest -s
        P1 = Point(46, 64)
        P2 = Point(98, 75)
        cls.__length = (45**2 + 49**2)**0.5
        cls.__mat = mock
        cls.__mat.E = 35000
        cls.__mat.alpha = 10 * 10**(-6)
        cls.__section = mock
        cls.__section.area = 11.33
        cls.__section.inertia_y = 25.5375
        cls.__section.h = 4.2
        cls.test = Barre(P1, P2, cls.__section, cls.__mat)

        P3 = Point(0, 0)
        P4 = Point(45, 49)

        cls.test.redefine_property(P3, P4, cls.__section, cls.__mat)

        del P1, P2, P3, P4

    @classmethod
    def teardown_class(cls):
        pass #print("après mon test unitaire", cls)
        del cls.test
        del cls.__length, cls.__mat, cls.__section

    def test_get_length(self):
        """ """
        assert self.test.length == self.__length

    def test_get_alpha(self):
        """ """
        assert self.test.angle == 47.43664824681013

    def test_get_rot_mat(self):
        """ """
        tmp = npsum(self.test.rot_mat)
        rslt = 4.705619998306716
        assert tmp == rslt

    def test_get_k_local_fixed_fixed(self):
        """ """
        self.test.define_local_mat("FIXED", "FIXED")
        tmp = npsum(self.test.k_local)
        rslt = 161221.13164910144
        assert tmp == rslt

    def test_get_k_local_pined_fixed(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_fixed_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "FIXED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_pined_pined(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("PINED", "PINED")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_local_lintel_linted(self):  # NotImplentedYet
        """ """
        # self.test.define_local_mat("LINTEL", "LINTEL")
        tmp = None  # npsum(self.test.K_local)
        rslt = None
        assert tmp == rslt

    def test_get_k_barre(self):
        """ """
        tmp = npsum(self.test.k_barre)
        rslt = 161221.13164910147
        assert tmp == rslt

    def test_uniform_load_fy_global_0(self):
        """ """
        py = -10
        self.test.uniforme_load(0, py, 0, "GLOBAL", 0)
        fx = 0
        fy = py * self.__length / 2
        mz = py * self.__length**2 / 12
        assert self.test.fy_x_beg == fx
        assert self.test.fy_y_beg == fy
        assert self.test.fy_m_beg == mz
        assert self.test.fy_x_end == fx
        assert self.test.fy_y_end == fy
        assert self.test.fy_m_end == -mz

    def test_uniform_load_fy_global_45(self):  # NotImplentedYet
        """ """
        py = -10
        angle = 45
        self.test.uniforme_load(0, py, 0, "GLOBAL", angle)
        fx = None
        fy = None
        mz = None
        # assert self.test.Fy_x_beg == fx
        # assert self.test.Fy_y_beg == fy
        # assert self.test.Fy_m_beg == mz
        # assert self.test.Fy_x_end == fx
        # assert self.test.Fy_y_end == fy
        # assert self.test.Fy_m_end == -mz

    def test_temperature_dt_x(self):
        """ """
        dt_x = 12  # °
        self.test.temperature(dt_x, 0)
        fx = self.__section.area * self.__mat.E * self.__mat.alpha * \
            dt_x / self.__length
        fy = 0
        mz = 0
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_temperature_dt_m(self): 
        """ """
        dt_m = 12  # °
        self.test.temperature(0, dt_m)
        fx = 0
        fy = 0
        mz = self.__section.inertia_y * self.__mat.E * self.__mat.alpha * \
            dt_m / self.__section.h
        assert self.test.dt_x_beg == fx
        assert self.test.dt_y_beg == fy
        assert self.test.dt_m_beg == mz
        assert self.test.dt_x_end == -fx
        assert self.test.dt_y_end == -fy
        assert self.test.dt_m_end == -mz

    def test_prestress_load(self):  # NotImplentedYet
        """ """
        pass
         # NotimplementedYet
