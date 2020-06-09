#-*- conding utf8 -*-

try:
	import numpy as np
	import sympy as sp

import math

class TConcrete:
    """
    """
    __Alpha_cc = 1 # N.A
    __Gamma_c = 1.5 #for persistent situation;
    #1.2 for Accidental situation

#---------------------
#   INITIALISATION   |
#---------------------                                          

    def __init__(self, material, fx, fy, mt):
        self.__Concrete_mat = material(0)
        self.__Steel_mat = material(1)
        
        self.define_lim()
        
        self.__Fx = fx
        self.__Fy = fy
        self.__Mt = mt
        
    def define_lim(self):
                
        epsilon_k = self.__Steel_mat.epsilon_k
        epsilon_p = self.__Steel_mat.epsilon_p
        epsilon_cu = self.__Concrete_mat.epsilon_cu
        xci_ab =  epsilon_cu / (epsilon_cu + epsilon_k)
        xci_p = epsilon_cu / (epsilon_cu + epsilon_p)
        
        self.__Lambda = self.__Concrete_mat.lamb
        self.__Eta = self.__Concrete_mat.eta
        self.__Mu_ab = xci_ab * self.__Lambda * self.__Eta * (1 - self.__Lambda*xi_ab / 2)
        self.__Mu_p = xci_p * self.__Lambda * self.__Eta * (1 - self.__Lambda*xi_p / 2)
        
#---------------------
#   CALCULATION      |
#---------------------

    # ULS
    def _Simple_bending_rect_ULS(self,overload="Ast"): # Ultimate limite state
        
        fcd = self.__Concrete_mat.fcd

        self.__Mu_edu = self.__Mt / (b*d*d*fcd)
        self.__Pivot = "A" if self.__Mu_edu <= self.__Mu_ab else "B" 

        xci_edu = (1-math.sqrt(1-2*self.__Mu_edu/self.__Eta))/self.__Lambda

        self.__X_edu = xci_edu*d

        self.__Z = d-self.__Lambda*self.__X_edu/2

        self.__epsilon_st = (1-xci_edu)*self.__ecu/(xci_edu)
        self.__Sigma_st = min(self.__Es*self.__epsilon_st, self.__fyd*1+(k-1)*(self.__epsilon_st-self.__epsilon_p)/(self.__epsilon_uk-self.__epsilon_p))
        self.__Ast = self.__Mu_edu/(self.__Z*self.__Sigma_st)
        
        if overload == "Ast":
            return self.__Ast
        elif overload == "":
            pass
    
    def _Compression(self):
        pass
    
    def _Traction(self):
        pass

    def _Torsion(self):
        pass
        
    # SLS
    def _stress_verification(self):
        pass
    
    def _Simple_bending_rect_SLS(self): # Service limite state
        pass    
    

    def _mecanical_percentage(self):
        
        self.__roh = self.__As/self.__Section

    def _mecanical_percentage(self):
        
        self.__omega = self.__roh*self.__fyd/self.__fcd

# Constant variable get

    @property
    def get_ALPHA_CC(self):
        return self.ALPHA_CC

    @property
    def get_GAMMA_C0(self):
        return self.GAMMA_C0
    
    @property
    def get_GAMMA_C1(self):
        return self.GAMMA_C1

    @property
    def get_GAMMA_C2(self):
        return self.GAMMA_C2

    @property
    def get_GAMMA_C3(self):
        return self.GAMMA_C3


class TBeam(TConcrete):
    """
        Class to e
    
    """
    def __init__(self, _fck, forces,_b,_h=0):
        super(TBeam,self).__init__(_fck, forces)
        if _h == 0:
            self.Radius = _b
        else:
            self.Base = _b
            self.Hight = _h

    def Asw(self): # longitudinal steel
        pass

    def Asfw(self): # 
        pass

    def L_Reinforment(self):
        pass

    def T_Reinforment(self):
        pass



class TColumn(TConcrete, TSteel):
    
#---------------------
#   INITIALISATION   |
#--------------------- 

    def __init__(self, _fck, _fyk, _l,_b,_h=0):
        TConcrete.__init__(_fck)
        TSteel.__init__(_fyk)
        if _h == 0:
            # self.Radius =
            pass 
        else:
            self.Base = _b
            self.Height = _h
            self.C_Area = _b*_h # Concrete area

    def __l0(self):
        pass

    def __i(self):
        self.i = math.sqrt(self.Ic/self.C_Area)


#---------------------
#   VERIFICATION     |
#---------------------

    def Geometric_Verification(self):
        if self.Length/self.Height < 3 and self.Height >= 4*self.Base:
            return False
        else:
            return True

#---------------------
#   CALCULATION      |
#---------------------


    def Slenderness_max(self):
        # TODO: if rectangle
        self.Lambda_max =
        # TODO: if circulare section
        self.Lambda_max = 4*self.L0/self.Radius

    def Slenderness_Lim(self, _phyef=0, _w=0, _rm=0):

            A = 0.7 if _phyef == 0 else 1/(1+0.2*_phyef)
            B = 1.1 if _w == 0 else math.sqrt(1+2*_w)
            C = 0.7 if _phyef == 0 else 1.7-self._rm
            n = Ned/(self.C_Area*self.Fcd)

            self.Lambda_Lim = 20*A*B*C/math.sqrt(n)

    def Slenderness(self):
        self.Lambda = self.l0/slef.i

    def Height_Calculation(self):

        self.C_Area = Ned/(self.Fcd+self.SigmaS/100)
        self.Height = self.C_Area/self.Base

    def L_Reinforcement(self): # Longiudinal reinforcment
        self.Fc = self.C_Area*self.Fcd
        self.Fs = Ned - self.Fc
        self.As = self.Fs/self.Sigma_S

    def L_Reinforcement_Min(self):
        self.As_min1 = 0.1*Ned/self.Fyd
        self.As_min2 = 0.2*self.C_Area/100

        self.As_min = (self.As_min1, self.As_min2)		

    def L_Reinforcement_Max(self, _recovery=False):

        self.As_max = self.C_Area*(0.04 if _recovery else 0.08)

    def T_Reinforcement_min(self):
        self.L_As_min = max(6,sectionacierlongitudinal/4)

    def T_Spacing_max(self):
        self.Spacing = min(20*sectionacierlongitudinal,
                        self.Base,
                        400)
    def T_Number(self):
        self. = self.Length/self.Spacing

class TSlab(TConcrete):

    def __init__(self, _b, _h):
        super(TSlab,self).__init__()
        self.Base = _b
        self.Hight = _h
           
if __name__ == "__main__":

    """
    sec = My_section()
    mat = My_material()
    
    force = (fx,fy,m)
    
    beam = my_beam(force,sec,mat)
    
    flex = simple_flex(beam) # Hyp 1
    beam.simple_flex(sortie) # Hyp 2
    
    
    """
