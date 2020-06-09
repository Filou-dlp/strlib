
import xlwings

class TExcel:

    def __init__(self, path): 
        self.__Path = path
    
    def define_variable(self):
        self.Prepo_ville = []
        self.Ville = []
        self.Prepo_dep = []
        self.Dep = []
        self.Prepo_reg = []
        self.Reg = []
        
        wb = xw.Book(self.__Path)
        
        for i in range(0,99999):
            self.Prepo_ville.append(wb.sheets['feuil1'].range((2+i,1)).value) # row, col
            self.Ville.append(wb.sheets['feuil1'].range((2+i,2)).value)
            self.Prepo_dep.append(wb.sheets['feuil1'].range((2+i,3)).value)
            self.Dep.append(wb.sheets['feuil1'].range((2+i,4)).value)
            self.Prepo_reg.append(wb.sheets['feuil1'].range((2+i,5)).value)
            self.Reg.append(wb.sheets['feuil1'].range((2+i,6)).value)
            
            
        