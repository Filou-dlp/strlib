#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module to make simple flexion ULS calculation
"""
import sys
import math

sys.path.append(sys.path[0]+'/../Office_lib')
print(sys.path)
#import TWord

class SimpleFlexureULS:
    """
        Class to calculate element in simple flexure ULS
    """
    def __init__(self, medu, cross_section, mat_steel, mat_concrete):
        """ Constructor
            :@param Medu: Moment inside the section
            :@param cross_section: section of the element
            :@param mat_steel: property of the reinforce steel
            :@param mat_concrete: property of the concrete
            :@type Medu: double
            :@type cross_section: TSection object
            :@type mat_steel: TMaterial object
            :@type mat_concrete: TMaterial object
        """

        self.__m_edu = medu

        self.__mat_steel = mat_steel
        self.__mat_concrete = mat_concrete

        self.__section = cross_section

        self.__b = self.__section.b

        self.__d = self.__section.d
        self.__d_p = self.__section.d_p
        self.__lambda = self.__mat_concrete.LAMBDA_RC
        self.__eta = self.__mat_concrete.ETA_RC

        # Variable that will be used
        self.__section_kind = None

        # mu
        self.mu_edu = None
        self.mu_ab = None
        self.mu_p = None

        # chi
        self.__chi_edu = None
        self.__chi_edu_comp = None
        self.__chi_p = None

        # Z
        self.z = None
        self.z_com = None

        # Mp
        self.mp = None

        # sigma
        self.sigma_st = None
        self.sigma_sc = None

        # As
        self.ast = None
        self.asc = None
        self.asmin = None
        self.asmax = None

        # roh
        self.roh = None

        # omega
        self.omega_st = None
        self.omega_sc = None

    def make_calculation(self, kind="RECT"):
        """
            function to make all calculation
            :@param kind: type of secion to make calculation
            :@param d: usefull heigth for tensil reinforcement
            :@param d_p: usefull heigth for compression reinforcement
            :@type kind: string
            :@type d: double
            :@type d_p: double
            :@default kind: RECT (mean rectangulare section, RANDOM for a random section)
            :@default d: 0 (take the default value .9*h)
            :@default d_p: 0 (take the default value .1*h)
        """
        if kind == "RECT":
            self.__section_kind = "RECT"

            self.__define_mu_ab()
            self.__define_mu_p()
            self.__define_mp()
            self.__define_mu_edu()
            self.__define_chi_edu()
            self.__define_z_edu()
            self.__define_sigma_st()

            if self.mu_edu <= self.mu_p:
                self.__define_ast()
            else:
                self.__define_sigma_sc()
                self.__define_ast()
                self.__define_asc()

            self.__define_mecanical_ratio()
            self.__define_geometrical_ratio()
            self.__define_asmin()
            self.__define_asmax()

        elif kind == "RANDOM":
            pass

    def __define_mu_ab(self):
        """ function to calculate mu_ab """
        epsilon_uk = self.__mat_steel.epsilon_uk
        epsilon_cu = self.__mat_concrete.epsilon_cu2

        chi_ab = epsilon_cu / (epsilon_uk + epsilon_cu)

        self.mu_ab = self.__lambda * chi_ab * self.__eta * \
                (1 - self.__lambda * chi_ab / 2)

    def __define_mu_p(self):
        """ Function to calculate mu_p """
        epsilon_p = self.__mat_steel.epsilon_p * 1000
        epsilon_c = self.__mat_concrete.epsilon_cu2

        self.__chi_p = epsilon_c / (epsilon_p + epsilon_c)

        self.mu_p = self.__lambda * self.__chi_p * self.__eta * \
                (1 - self.__lambda * self.__chi_p / 2)

    def __define_mp(self):
        """ Function to define Plastique moment """
        self.mp = self.mu_p * self.__b * self.__d**2 * \
                self.__mat_concrete.fcd

    def __define_mu_edu(self):
        """ function to calculate mu_edu """
        if self.__section_kind == "RECT":
            fcd = self.__mat_concrete.fcd

            self.mu_edu = self.__m_edu / (self.__b * self.__d**2 * fcd)

        elif self.__section_kind == "RANDOM":
            pass

    def __define_chi_edu(self):
        """ function to calculate mu_edu """
        if self.mu_edu > self.mu_p:
            mu_edu = self.mu_p
            self.__chi_edu_comp = (1 - math.sqrt(1 - 2 * \
                (self.mu_edu - self.mu_p) / self.__eta)) / self.__lambda

        else:
            mu_edu = self.mu_edu

        self.__chi_edu = (1 - math.sqrt(1 - 2 * mu_edu / self.__eta)) / \
                self.__lambda

    def __define_z_edu(self):
        """
            function to calculate z
            also for case with compressive steel
        """
        self.z = self.__d*(1 - self.__lambda * self.__chi_edu / 2)

        self.z_com = self.__d - self.__d_p

    def __define_sigma_st(self):
        """ function to calculate sigma_st """
        epsilon_cu = self.__mat_concrete.epsilon_cu2
        epsilon_uk = self.__mat_steel.epsilon_uk
        Es = self.__mat_steel.E
        fyd = self.__mat_steel.fyd
        
        if self.mu_edu <= self.mu_p:
            if self.mu_edu <= self.mu_ab:
                epsilon_st = self.__mat_steel.epsilon_uk # A Vérifier

            else:
                epsilon_st = (1 - self.__chi_edu) * epsilon_cu / self.__chi_edu

            k = self.__mat_steel.k

            epsilon_p = self.__mat_steel.epsilon_p

            self.sigma_st = min(Es * epsilon_st, fyd * (1 + (k - 1) * \
                        (epsilon_st - epsilon_p) / (epsilon_uk - epsilon_p)))
        else:
            self.sigma_st = fyd

    def __define_sigma_sc(self):
        """
            function to calculate sigma_sc
            for compressive steel
        """
        fyd = self.__mat_steel.fyd
        delta = self.__d_p / self.__d

        epsilon_cu = self.__mat_concrete.epsilon_cu2
        epsilon_sc = (self.__chi_edu - delta) * \
                epsilon_cu / self.__chi_edu
        epsilon_p = self.__mat_steel.epsilon_p
        epsilon_uk = self.__mat_steel.epsilon_uk
        k = self.__mat_steel.k

        self.sigma_sc = fyd * min(epsilon_sc / epsilon_p, 1 + (k - 1) * \
                ((epsilon_sc - epsilon_p) / (epsilon_uk - epsilon_p)))

    def __define_ast(self):
        """
            function to calculate Ast
            with or without compression reinforcement
        """
        if self.mu_edu <= self.mu_p:
            self.ast = self.__m_edu / (self.z * self.sigma_st)
        else:
            self.ast = self.mp / (self.z * self.sigma_st) + \
                    (self.__m_edu - self.mp) / (self.z_com * self.sigma_sc) *\
                        self.sigma_st / self.sigma_sc

    def __define_asc(self):
        """ function to calculate Asc """
        self.asc = (self.__m_edu - self.mp) / (self.z_com * self.sigma_sc)

    def __define_mecanical_ratio(self):
        """ function to calculate omega """
        if self.__section_kind == "RECT":
            if self.mu_edu <= self.mu_p:
                fyd = self.__mat_steel.fyd
                self.omega_st = self.__eta * self.__lambda * \
                        self.__chi_edu * fyd / self.sigma_st
            else: # A vérifier
                delta = self.__d_p / self.__d
                fyd = self.__mat_steel.fyd
                mu_cp_sup = self.__eta * self.__lambda * self.__chi_p * \
                        (delta - self.__lambda * self.__chi_p / 2)
                mu_cp_inf = self.mu_p

                self.omega_st = (self.mu_edu - mu_cp_sup) / (1 - delta)
                self.omega_sc = (self.mu_edu - mu_cp_inf) / \
                        ((1 - delta) * self.sigma_sc / fyd)
        else:
            pass

    def __define_geometrical_ratio(self):
        """ function to calculate roh """
        if self.__section_kind == "RECT":
            if self.mu_edu <= self.mu_p:
                fcd = self.__mat_concrete.fcd
                self.roh = self.__eta * self.__lambda * \
                        self.__chi_edu * fcd / self.sigma_st
            else: # A vérifier
                fcd = self.__mat_concrete.fcd
                fyd = self.__mat_steel.fyd

                self.roh = (self.omega_st + self.omega_st) * fcd / fyd
        else:
            pass

    def __define_asmin(self):
        """ function to calculate Asmin """
        fctm = self.__mat_concrete.fctm
        fyk = self.__mat_steel.fyk

        self.asmin = max(0.26 * fctm * self.__b * self.__d / fyk, \
                0.0013 * self.__b * self.__d)

    def __define_asmax(self):
        """ function to calculate Asmax """
        self.asmax = 0.4 * self.__section.area

    def calculation_note_fr(self, name, office="WORD"):
        """
            Function to make a calculation note with word
            :@param name: Name of the calculation note
            :@type name: string
        """
        if self.__section_kind == "RECT":
            my_doc = TWord.TWord(name, office)
            my_doc.create()

            my_doc.title("Note de calcul en flexion simple ELU", lvl=0)
            my_doc.title("Hypothèse", lvl=1)

            my_doc.title("Section", lvl=2)
            my_doc.paragraphe("b = " + self.__section.b + " m")
            my_doc.paragraphe("h = " + self.__section.h + " m")
            my_doc.paragraphe("Air = " + self.__section.Area + " m²")
            if self.__d == self.__section.h * 0.9:
                my_doc.paragraphe("d = 0.9*h = " + self.__d + \
                        " m" + " (En première approhe)")
            else:
                my_doc.paragraphe("d = " + self.__d + " m")

            if self.__d_p == self.__section.h * 0.1:
                my_doc.paragraphe("d = 0.1*h = " + self.__d_p + \
                        " m" + " (En première approhe)")
            else:
                my_doc.paragraphe("d = " + self.__d_p + " m")

            my_doc.title("Matériaux", lvl=2)
            my_doc.paragraphe("Béton C" + self.__mat_concrete.fck)
            my_doc.paragraphe("Acier FE" + self.__mat_steel.fyk + \
                    self.__mat_steel.k)
            my_doc.paragraphe("μp = " + round(self.mu_p, 3))
            my_doc.paragraphe("μab = " + round(self.mu_ab, 3))

            my_doc.title("Charge", lvl=2)
            my_doc.paragraphe("Medu = " + self.__m_edu + " MN.m")

            my_doc.title("Calcul", lvl=1)
            my_doc.paragraphe("μedu = " + round(self.mu_edu, 3))
            if self.mu_edu <= self.mu_ab:
                my_doc.paragraphe("μedu <= μab => Pivot A")
            else:
                my_doc.paragraphe("μedu > μab => Pivot B")

            if self.mu_edu <= self.mu_p:
                my_doc.paragraphe("μedu <= μp => Pas d'acier comprimé")
                my_doc.paragraphe("z = " + round(self.z, 3)+" m")
                my_doc.paragraphe("σst = " + round(self.sigma_st, 3) + " MPa")
                my_doc.paragraphe("Ast = " + \
                        round(self.ast * 10**(-4), 3) + " cm²")

            else:
                my_doc.paragraphe("μedu > μp => Présence d'acier comprimé")
                my_doc.paragraphe("z1 = " + round(self.z, 3)+" m")
                my_doc.paragraphe("zcomp = " + round(self.z_com, 3)+" m")
                my_doc.paragraphe("σst = " + \
                        round(self.sigma_st, 3) + " MPa")
                my_doc.paragraphe("σsc = " + \
                        round(self.sigma_sc, 3) + " MPa")
                my_doc.paragraphe("Ast = " + \
                        round(self.ast * 10**(-4), 3) + " cm²")
                my_doc.paragraphe("Asc = " + \
                        round(self.asc * 10**(-4), 3) + " cm²")

            my_doc.paragraphe("Pourcentage mécanique = " + \
                    round((self.omega_sc + self.omega_st) / 100, 3) + " %")
            my_doc.paragraphe("Pourcentage géométrique = " + \
                    round((self.roh / 100), 3) + " %")

            my_doc.title("Acier minimaux", lvl=1)
            my_doc.paragraphe("Asmin = " + \
                    round(self.asmin * 10**(-4), 3) + " cm²")

            my_doc.save()
            my_doc.close()
