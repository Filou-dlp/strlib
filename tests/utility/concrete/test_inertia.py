import sys
sys.path.append(sys.path[0]+'/../../../strlib')
from utility.concrete.inertia import IntertiaRect, IntertiaTRect


class TestInertiaRect:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        b = 20
        h = 40
        alpha_eq = 15
        d = 0.9 * h
        ast = 10 * 10**-4 
        d_p = 0.1 * h
        asc =  5 * 10**-4 

        cls.test = IntertiaRect(b, h, alpha_eq, d, ast, d_p, asc)
        cls.test.make_calculation()

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
    
    def test_x_homogenous(self):
        """ """
        rslt = 20.000149995781367
        assert self.test.x_homogenous == rslt

    def test_inertia_homogenous(self):
        """ """
        rslt = 106672.42664866717
        assert self.test.inertia_homogenous == rslt

    def test_x_crack(self):
        """ """
        rslt = 0.23762437827144184
        assert self.test.x_crack == rslt

    def test_inertia_crack(self):
        """ """
        rslt = 19.37982896260232
        assert self.test.inertia_crack == rslt


class TestInertiaTRect:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)
        bw = 20
        beff = 100
        h = 40
        hf = 0.2
        alpha_eq = 15
        d = 0.9 * h
        ast = 10 * 10**-4
        d_p = 0.1 * h
        asc =  5 * 10**-4
    
        cls.test = IntertiaTRect(bw, beff, h, hf, alpha_eq, d, ast, d_p, asc)
        cls.test.make_calculation()

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)

    def test_x_homogenous(self):
        """ """
        rslt = 19.609961735123726
        assert self.test.x_homogenous == rslt

    def test_inertia_homogenous(self):
        """ """
        rslt = 59195.35600147059
        assert self.test.inertia_homogenous == rslt

    def test_x_crack(self):
        """ """
        rslt = 0.07527367962421595
        assert self.test.x_crack == rslt

    def test_inertia_crack(self):
        """ """
        rslt = 21.983438147222916
        assert self.test.inertia_crack == rslt
