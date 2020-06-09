
try:
	import numpy as np
	import sympy as sp
except:
	pass

class TLoad:

#---------------------
#	INITIALISATION   |
#---------------------

	def __init__(self, _load=0):
	
		if _load == 0:
			self.Ned = _load[0]
			self.Ved = _load[1]
			self.Med = _load[2]
			self.Alpha = _load[3]

#---------------------
#	SET Variable     |
#---------------------

	def set_Ned(self, _ned):
		self.Ned = _ned
	
	def set_Ved(self, _ved):
		self.Ved = _ved
	
	def set_Med(self, _med):
		self.Med = _med
	
	def set_Alpha(self, _alpha):
		self.Alpha = _alpha

class TCombinaison:

	GAMMA_SUP = 1.35
	GAMMA_INF = 1
	GAMMA_VAR = 1.5

#---------------------
#	INITIALISATION   |
#---------------------  

	def __init__(self, _perm, _variable):
		"""
			Constructor
			
			@param _perm 
			@type str
			
			@param _variable
			@type dict
		"""
		self.Perm_Load = _perm
		self.Variable_Load = _variable
	
	def Permanante(self):
	
		dict = {}
		for i in range(len(self.Variable_Load)):
		
			_tmp_dict = self.Variable_Load.copy()
			_sum = 0
			del _tmp_dict[str(i+1)]
			for key, value in _tmp_dict.items():
				_sum += value [0]*value[1]
			
			self.Combine_Load = self.GAMMA_SUP*self.Perm_Load + self.GAMMA_VAR*self.Variable_Load[str(i+1)][0] + _sum
			dict[i] = self.Combine_Load

		return dict
		
		

#---------------------
#	GET Variable     |
#---------------------

# Constant variable update

	@property
	def get_GAMMA_SUP(self):
		return self.GAMMA_SUP
	
	@property
	def get_GAMMA_INF(self):
		return self.GAMMA_INF
#---------------------
#	UPDATE Variable  |
#---------------------

# Constant variable update


	def update_GAMMA_SUP(self, _tmp):
		self.GAMMA_SUP = _tmp
	

	def update_GAMMA_INF(self, _tmp):
		self.GAMMA_INF = _tmp
		
class TSnow(TCombinaison):

	def __init__(self):
		super(TSnow,self).__init__()

class TWind(TCombinaison):

	def __init__(self):
		super(TWind,self).__init__()
		
if __name__  == "__main__":

	_tmp = TCombinaison(10,{"1": (1,0.8), "2": (2,0.7) })
	a = _tmp.Permanante()
	print(a)