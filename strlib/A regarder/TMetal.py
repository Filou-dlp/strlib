
import math
import sympy


class TSteel:

	GAMMA_M0 = 1.15
	GAMMA_M1 = 0 
	GAMMA_M2 = 0

#---------------------
#	INITIALISATION   |
#---------------------

	def __init__(self, matetrial, cross_section, _load[]):
		self.__Cross_section = cross_section
		self.__Material = matetrial


		self.__define_value()
	
		self.__Fyk = self.__Material.Fyk

		self.__Var_Calc()
		self.N = _load[0]
		self.Ty = _load[1]
		self.Tz = _load[2]
		self.Myy = _load[3]
		self.Mzz = _load[4]
		
	
	def __define_value(self):
		A = self.__Cross_section.Area
		Wel = self.__Cross_section.Wel
		Wpl = self.__Cross_section.Wpl

		self.__Nplrd = A*self.Fy/self.__GAMMA_MO
	
		self.__Melrd = Wel*self.Fy/self.__GAMMA_MO
		self.__Mplrd = Wpl*self.Fy/self.__GAMMA_MO

	def kind_calculation(self):
		"""
		
		"""
		
		_tmp = ("Compression/traction", "Flexion simple", "Flexion composée")
		
		return _tmp

#---------------------
#	CALCULATION      |
#---------------------

	def __Var_Calc(self): # __ for say "it's private"
		self.__fyd()
		self.__Es()
		self.__Full_Section()
		self.__Bolt_Section()
	
	def __Full_Section(self):
		
		self.Nplrd = A*self.Fy/self.GAMMA_MO
	
	def __Bolt_Section(self):
		self.Nurd = A*self.Fy/self.GAMMA_MO
		
	def __Flexion_Simple(self, _axes = "Y" ,_txt=False)
	
		if _txt:
			ntext = []
			ntext.append("MRd,el,y = Wel,y*fy/γM0 =") # Class 3
			ntext.append("MEd,y,/MRd,el =")
			return ntext
		
		if _axes.upper() == "Y":
			self.Fsy = self.MRd_y/self.Myy 
		elif _axes.upper() == "Z":
			self.Fsz = self.MRd_z/self.Mzz 
	
	def __Effort_tranchant

#---------------------
# Feature calculation|
#---------------------

	def __fyd(self):
		self. Fyd = self.Fyk/self.GAMMA_M0
	
	def __Es(self):
		self.Es = 210000 # MPa

#---------------------
#	GET Variable     |
#---------------------
	
	@property
	def get_fyd(self):
		return self.Fyd
	@property
	def get_Anet(self):
		return self.Anet
	
	@property
	def get_As(self):
		return self.As

#---------------------
#	UPDATE Variable  |
#---------------------		

	def update_Fyk(self, _tmp):
		self.Fyk = _tmp
		self.__Var_Calc()
	
# Constant variable update

	def update_GAMMA_MO(self, _gamma_mo):
		self.GAMMA_MO = _gamma_mo
	
	def update_GAMMA_M1(self, _gamma_m1):
		self.GAMMA_M1 = _gamma_m1

	def update_GAMMA_M2(self, _gamma_m2):
		self.GAMMA_M1 = _gamma_m2
		
#---------------------
#	SET Variable     |
#---------------------

	def set_As(self, _as):
		self.As = _as
	
	def set_Number(self, _nb)
		self.S_Nb = _nb

class TBeam(TSteel):

#---------------------
#	INITIALISATION   |
#---------------------

	def __init__(self, _fyk):
		super(TBeam,self).__init(_fyk)

#---------------------
#	CALCULATION      |
#---------------------
		
	def Full_Section(self):
		"""
		
		"""

		self.Nplrd = A*self.Fy/self.GAMMA_MO
	
	def Full_Section(self):
		self.Nurd = A*self.Fy/self.GAMMA_MO

#---------------------
#	GET Variable     |
#---------------------
		
	@property
	def get_Nplrd(self):
		return self.Nplrd
	
	@property
	def get_Nurd(self):
		return self.Nurd



		
class TColumn(TSteel):

	def __init__(self):
		super(TColumn,self).__init__()
		
class TSlab(TSteel):

	def __init__(self):
		super(TSlab, self).__init__()

	
