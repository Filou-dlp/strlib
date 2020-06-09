# Librairy
import timeit
start = timeit.default_timer()

import sys, os
import copy

# import sympy as sp
import math
import numpy as np

#try:
#    import TSection as sec
#except:
#    print("Can't import TSection")

#try:
#    import TMaterial as mat
#except:
#    print("Can't import TMaterial")

print("Librairy importation: " + str(timeit.default_timer()-start))

class TPoint:
    """
        Class to define point element:
        FEM
        Cross section

        This class can be define a "symbolic class"
        it's mean that all calculation will be algerbric

        :@param __NB_POINT: Nb of point created
        :@type __NB_POINT: integer
        :@default name: 0 (No elements created)

    """
    NB_POINT = 0

    def __init__(self, x, y, name=0, symbolic=False):
        """ Constructor 
            :@param x: X coordonate
            :@param y: Y coordonate
            :@param name: Node name
            :@param symbolic: Choose if all calculation will be algerbric
            :@type x: double
            :@type y: double
            :@type name: double
            :@type symbolic: boolean
            :@default name: 0 (No name given)
            :@default symbolic: False (Numerical calculation)
        """
        TPoint.NB_POINT += 1
        self.__Symbolic_class = symbolic

        # Coordonate
        if symbolic:
            raise NotImplementedError("Not implented yet")
            self.__define_default_value_symb(name)
        else:
            self.__X = x
            self.__Y = y
            self.__Pt_num = TPoint.NB_POINT
            self.__define_default_value(name)
    
    def __define_default_value(self,name):
        """ Initialize default value  
            :@param name: Point Name
            :@type name: String
        """
        
        # Set value as P_number by default
        if name == 0:
            self.__Name = "P" + str(TPoint.NB_POINT) 
        else: # Other the name choosen
            self.__Name = name
        
        self.__Rx = 0
        self.__Ry = 0
        self.__Mt = 0

        self.__Delta_x = 0
        self.__Delta_y = 0
        self.__Rot = 0
        
        # False mean any support
        self.__Rx_cond = 0
        self.__Ry_cond = 0
        self.__Mt_cond = 0
        
        self.__Fx = 0
        self.__Fy = 0
        self.__Mz = 0
        
    def define_external_force(self, fx, fy, mz):
        """ Function to define external force 

            :@param fx: External force in X
            :@param fy: External force in Y
            :@param mz: External moment in Z
            :@type fx: double
            :@type fy: double
            :@type mz: double
        """

        self.__Fx = fx
        self.__Fy = fy
        self.__Mz = mz

    def define_internal_force(self, fx, fy, mz):
        """ Function to define external force 
        
            :@param fx: Normal node force
            :@param fy: Shear node force
            :@param mz: Moment node force
            :@type fx: double
            :@type fy: double
            :@type mz: double
        """

        self.__Normal = fx
        self.__Shear = fy
        self.__Moment = mz
    
    def define_support_reaction(self, rx, ry, mt):
        """ Function to define support reaction 
        
            :@param rx: X reaction
            :@param ry: Y reaction
            :@param mt: Moment reaction
            :@type rx: double
            :@type ry: double
            :@type mt: double
        """

        self.__Rx = rx
        self.__Ry = ry
        self.__Mt = mt
    
    def define_displacement(self, dx, dy, theta):
        """ Function to define displacement 
        
            :@param dx: X displacement
            :@param dy: Y displacement
            :@param theta: rotation
            :@type dx: double
            :@type dy: double
            :@type theta: double
        """

        self.__Delta_x = dx
        self.__Delta_y = dy
        self.__Rot = theta
    
    def define_support_condition(self, rx=False, ry=False, mt=False):
        """ Function to define displacement 
        
            :@param rx: Block X displacement (True)
            :@param ry: Block Y displacement (True)
            :@param mt: Block rotation (True)
            :@type rx: bool
            :@type ry: bool
            :@type mt: bool
            :@default rx: False (Allow displacement)
            :@default ry: False (Allow displacement)
            :@default mt: False (Allow rotation)
        """
        self.__Rx_cond = 1 if rx else 0
        self.__Ry_cond = 1 if ry else 0
        self.__Mt_cond = 1 if mt else 0
        

# Set 
 # Name
    def __set_Name(self, name):
        self.__Name = name
 # Pt_num
    def __set_Pt_num(self,val):
        self.__Pt_num = val
 # Support reaction
    def __set_Rx(self, val):
        self.__Rx = val
    def __set_Ry(self,val):
        self.__Ry = val
    def __set_Mt(self,val):
        self.__Mt = val

 # Displacement
    def __set_Dx(self,val):
        self.__Delta_x = val
    def __set_Dy(self,val):
        self.__Delta_y = val
    def __set_Theta(self,val):
        self.__Rot = val

# Get
 # Name
    def __get_Name(self):
        return self.__Name
 # Pt_num
    def __get_Pt_num(self):
        return self.__Pt_num

 # Coordonate
    def __get_Y(self):
        return self.__Y
    def __get_X(self):
        return self.__X
    
 # External force
    def __get_Fx(self):
        return self.__Fx
    def __get_Fy(self):
        return self.__Fy
    def __get_Mz(self):
        return self.__Mz

 # Internal force
    def __get_Normal(self):
        return self.__Normal
    def __get_Shear(self):
        return self.__Shear
    def __get_Moment(self):
        return self.__Moment
    
 # Support reaction
    def __get_Rx(self):
        return self.__Rx
    def __get_Ry(self):
        return self.__Ry
    def __get_Mt(self):
        return self.__Mt

    def __get_Rx_cond(self):
        return True if self.__Rx_cond == 1 else False
    def __get_Ry_cond(self):
        return True if self.__Ry_cond == 1 else False
    def __get_Mt_cond(self):
        return True if self.__Mt_cond == 1 else False

 # Displacement
    def __get_Dx(self):
        return self.__Delta_x
    def __get_Dy(self):
        return self.__Delta_y
    def __get_Theta(self):
        return self.__Rot

 # Other
    def __get_Sum_support(self):
        counter_ = 0
        if self.__Rx_cond == True:
            counter_ += 1
        if self.__Ry_cond == True:
            counter_ += 1
        if self.__Mt_cond == True:
            counter_ += 1
        return counter_ 
           
 # Property
 
    X = property(__get_X)
    Y = property(__get_Y)
    Name = property(__get_Name, __set_Name)
    Pt_num = property(__get_Pt_num, __set_Pt_num)
    
    Fx = property(__get_Fx)
    Fy = property(__get_Fy)
    Mz = property(__get_Mz)
    
    Normal = property(__get_Normal)
    Shear = property(__get_Shear)
    Moment = property(__get_Moment)
    
    Rx = property(__get_Rx,__set_Rx)
    Ry = property(__get_Ry,__set_Ry)
    Mt = property(__get_Mt,__set_Mt)
    
    Rx_cond = property(__get_Rx_cond)
    Ry_cond = property(__get_Ry_cond)
    Mt_cond = property(__get_Mt_cond)
    
    Delta_x = property(__get_Dx,__set_Dx)
    Delta_y = property(__get_Dy,__set_Dy)
    Theta = property(__get_Theta,__set_Theta)
    
    Hyper_degree = property(__get_Sum_support)
    
class TBarre: 
    """
        Class to create barre element  
        according to 2 points

        :@param __NB_BARRE: Nb of element created
        :@type __NB_BARRE: integer
        :@default __NB_BARRE: 0 (No elements created)
    """
# Attribute
    NB_BARRE = 0 

    def __init__(self,  point1, point2, section=False, material=False, beg_type_="FIXED", end_type_="FIXED", symbolic=False):
        """ Constructor
            :@param point1: 1st node of the barre
            :@param point2: last node of the barre
            :@param section: Barre cross_section
            :@param material: Barre material
            :@param beg_type_: 1st node support condition for calculation
            :@param end_type_: last node support condition for calculation
            :@param symbolic: Choose if all calculation will be algerbric
            :@type point1: TPoint object
            :@type point2: TPoint object
            :@type section: TCross_section object or boolean
            :@type material: TMaterial object or boolean
            :@type beg_type_: String
            :@type end_type_: String
            :@type symbolic: boolean
            :@default section: False (mean we take A and I = 1)
            :@default material: False (mean we take E = 1)
            :@default beg_type_: "FIXED" (Node condition for the matrix creation)
            :@default end_type_: "FIXED" (Node condition for the matrix creation)
            :@default symbolic: False (Numerical calculation)
        """
        TBarre.NB_BARRE += 1

        # Point
        self.__P_beg = point1
        self.__P_end = point2
        
        self.__beg_type_ = beg_type_
        self.__end_type_ = end_type_
        
        self.__Pt_local_beg = self.__P_beg
        self.__Pt_local_end = self.__P_end
        
        # Section property
        self.__Cross_section = section
        self.__Material = material

        if symbolic:
            raise NotImplementedError("Not implented yet")
        else:
            self.__default_value()
            self.define_property()

# Initialisation

    def define_property(self):
        """ Function to define point property """
        self.__P_beg_name = self.__P_beg.Name
        self.__P_end_name = self.__P_end.Name
        
        self.__Pt_num_beg = self.__P_beg.Pt_num
        self.__Pt_num_end = self.__P_end.Pt_num
        
        self.__define_alpha()
        self.__define_length()
        self.__define_rotation_mat()
        self.define_local_mat(self.__beg_type_, self.__end_type_)
        
    def redefine_force(self):
        """ Function to redifine property after a split """
        fx = self.__Fx_force
        fy = self.__Fy_force
        mz = self.__Mz_force
        type = self.__Type_force
        angle = self.__Angle_force

        self.uniforme_load(fx,fy,mz,type,angle)
        
        dT_x = self.__dT_force_x
        dT_m = self.__dT_force_m
        
        self.temperature(dT_x,dT_m)
        
        eq = self.__PC_equation
        PC_value = self.__PC_value
        coef = self.__PC_coef
        kind = self.__PC_kind
        
        self.prestress_load(eq, kind, coef, PC_value)

    def __default_value(self):
        """ Function to define default value """
        self.__Fx = False
        self.__Fy = False
        self.__Mz = False
        self.__dT_x = False
        self.__dT_m = False
        self.__PC = False

        self.__Fx_force = 0
        self.__Fy_force = 0
        self.__Mz_force = 0
        self.__Type_force = "GLOBAL"
        self.__Angle_force = 0
        
        self.__dT_force_x = 0
        self.__dT_force_m = 0
        
        self.__PC_equation = 0
        self.__PC_value = 0
        self.__PC_coef = 0
        self.__PC_kind = 0
        
        # Fx
        self.__Fx_x_beg = 0 
        self.__Fx_y_beg = 0
        self.__Fx_m_beg = 0
        
        self.__Fx_x_end = 0 
        self.__Fx_y_end = 0
        self.__Fx_m_end = 0
      
        # Fy
        self.__Fy_x_beg = 0 
        self.__Fy_y_beg = 0
        self.__Fy_m_beg = 0
        
        self.__Fy_x_end = 0 
        self.__Fy_y_end = 0
        self.__Fy_m_end = 0

        # Mz
        self.__Mz_x_beg = 0 
        self.__Mz_y_beg = 0
        self.__Mz_m_beg = 0
        
        self.__Mz_x_end = 0 
        self.__Mz_y_end = 0
        self.__Mz_m_end = 0
        
        # dt
        self.__dT_x_beg = 0
        self.__dT_y_beg = 0
        self.__dT_m_beg = 0
        
        self.__dT_x_end = 0 
        self.__dT_y_end = 0
        self.__dT_m_end = 0
        
        # PC
        self.__PC_x_beg = 0
        self.__PC_y_beg = 0
        self.__PC_m_beg = 0
        
        self.__PC_x_end = 0 
        self.__PC_y_end = 0
        self.__PC_m_end = 0
        
    def __define_length(self):
        """ Function to define the length of the barre """
        x_beg_ = self.__P_beg.X
        y_beg_ = self.__P_beg.Y

        x_end_ = self.__P_end.X
        y_end_ = self.__P_end.Y
        
        self.__Length = math.sqrt((x_end_-x_beg_)**2 + (y_end_-y_beg_)**2)
    
    def __define_alpha(self):
        """ Function to define the angle of the barre 
            compare to a default axe |_ -> _ (x) ; | (y)
        """
        x_beg_ = self.__P_beg.X
        y_beg_ = self.__P_beg.Y

        x_end_ = self.__P_end.X
        y_end_ = self.__P_end.Y
        
        if (x_end_-x_beg_) != 0:
            atan_ = math.atan((y_end_-y_beg_)/(x_end_-x_beg_))
            angle_ = math.degrees(atan_)
        else:
            sign_ = math.copysign(1,(y_end_-y_beg_))
            angle_ = sign_ * 90
        
        self.__Angle = angle_
        
 # Define matrix
   
    def __define_rotation_mat(self):
        """ Function to define the rotation mat 
            __Rot_mat = [[ cos alpha, sin alpha, 0, 0, 0, 0],
                         [ -sin alpha, cos alpha, 0, 0, 0, 0],
                         [ 0, 0, 1, 0, 0, 0],
                         [ 0, 0, 0, cos alpha, sin alpha, 0],
                         [ 0, 0, 0, -sin alpha, cos alpha, 0],
                         [ 0, 0, 0, 0, 0, 1]] 
        """
        angle_rad_ = math.radians(self.__Angle)
        
        cos_, sin_ = math.cos(angle_rad_), math.sin(angle_rad_)
        
        self.__Rot_mat = np.array([[ cos_, sin_, 0, 0, 0, 0],
                         [ -sin_, cos_, 0, 0, 0, 0],
                         [ 0, 0, 1, 0, 0, 0],
                         [ 0, 0, 0, cos_, sin_, 0],
                         [ 0, 0, 0, -sin_, cos_, 0],
                         [ 0, 0, 0, 0, 0, 1]], dtype=float)

    def define_local_mat(self, beg_type_="FIXED", end_type_="FIXED"):
        """ Function to define local stiffness matrix to all element
            in local axes
            :@param beg_type_: 1st node of the barre
            :@param end_type_: 1st node of the barre
            :@type beg_type_: String
            :@type end_type_: String
            :@default beg_type_: FIXED (for frame element)
            :@default end_type_: FIXED (for frame element)
            :@other beg_type_: Pined (Truss element); LINTEL (Lintel element)
            :@other end_type_: Pined (Truss element); LINTEL (Lintel element)
        """
        
        l_ = self.__Length
        # Coefficient
        if self.__Material == False and self.__Cross_section == False:
            eal_ = 1 * 1 / l_
            ei_ = 1 * 1
        else:
            eal_ = self.__Material.E * self.__Cross_section.Area / l_
            ei_ = self.__Material.E * self.__Cross_section.Inertia_y
        
        # Matrix definition 
        if beg_type_ == "FIXED" and end_type_ == "FIXED":
            self.__k_local = np.array([
                [eal_, 0, 0, -eal_, 0, 0], 
                [0, 12* ei_/(l_**3), 6*ei_/(l_**2), 0, -12*ei_/(l_**3),6*ei_/(l_**2)],
                [0, 6*ei_/(l_**2), 4*ei_/l_,0 , -6*ei_/(l_**2), 2*ei_/l_],
                [-eal_, 0, 0, eal_,0,0],
                [0, -12* ei_/(l_**3), -6*ei_/(l_**2), 0, 12*ei_/(l_**3),-6*ei_/(l_**2)],
                [0, 6*ei_/(l_**2), 2*ei_/l_,0 , -6*ei_/(l_**2), 4*ei_/l_]], dtype=float )
        elif beg_type_ == "PINED" and end_type_ == "FIXED": # Need a vérification
            self.__k_local = np.array([ 
                [eal_, 0, 0, -eal_,0,0],
                [0, 3* ei_/(l_**3), 0, 0, -3*ei_/(l_**3),3*ei_/(l_**2)],
                [0, 0, 0, 0 , 0, 0],
                [-eal_, 0, 0, eal_,0,0],
                [0, -3* ei_/(l_**3), 0, 0, 3*ei_/(l_**3),-3*ei_/(l_**2)],
                [0, 3*ei_/(l_**2), 0, 0 , -3*ei_/(l_**2), 3*ei_/l_]], dtype=float)

        elif beg_type_ == "FIXED" and end_type_ == "PINED": # Need a vérification
            self.__k_local = np.array([ 
                [eal_, 0, 0, -eal_,0,0],
                [0, 3* ei_/(l_**3), 3* ei_/(l_**2), 0, -3*ei_/(l_**3),0],
                [0, 3* ei_/(l_**2), 3* ei_/l_, 0 , -3* ei_/(l_**2), 0],
                [-eal_, 0, 0, eal_,0,0],
                [0, -3* ei_/(l_**3), -3* ei_/(l_**2), 0, 3*ei_/(l_**3),0],
                [0, 0, 0, 0 , 0, 0]], dtype=float)
        elif beg_type_ == "PINED" and end_type_ == "PINED":
            self.__k_local = np.arra([ 
                [eal_, 0, 0, -eal_,0,0],
                [0, 0, 0, 0, 0,0],
                [0, 0, 0, 0 , 0, 0],
                [-eal_, 0, 0, eal_,0,0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0 , 0, 0]], dtype=float)
        
        elif beg_type_ == "LINTEL" and end_type_ == "LINTEL": # Need a vérification - HB IGH
            self.__k_local = np.arra([
                [0, 0, 0, 0, 0, 0]
                [0, 3, 3*(b1+a),0 ,-3 ,3(b2+a)]
                [0, 3*(b1+a), 3*b1**2+6*a*b1+4*a**2, 0, -3*(b1+a), 3*(b1+a)*(b2+a)- a**2]
                [0, 0, 0, 0, 0, 0,]
                [0, -3, -3*(b1+a), 0, 3, 3*(b2+a)]
                [0, 3*(b2+a), 3*(b1+a)*(b2+a)-a**2, 0, 3*(b2+a), 3*b2**2+6*a*b2+4*a**2]], dtype=float)
        
        self.__define_k_barre_mat()

    def __define_k_barre_mat(self):
        """ Function to define local stiffness matrix to all element
            in global axes
        """
        rot_t_ = np.transpose(self.__Rot_mat)
        self.__K_barre = np.matmul( \
                    np.matmul(rot_t_, self.__k_local), \
                    self.__Rot_mat)
    
    def uniforme_load(self, fx, fy, mz, type="GLOBAL", angle=0):
        """ Function to define uniforme load on the barre
        
            fx, fy, mz are global value

            :@param fx: uniforme fx
            :@param fy: uniforme fy
            :@param mz: uniforme mz
            :@type fx: double
            :@type fy: double
            :@type mz: double
        """
        l_ = self.__Length   

        angle_barre_rad_ = math.radians(self.__Angle)
        cos_barre_ = math.cos(angle_barre_rad_)
        sin_barre_ = math.sin(angle_barre_rad_)
        
        self.__Fx = True if fx != 0 else False
        self.__Fy = True if fy != 0 else False
        self.__Mz = True if mz != 0 else False
        
        self.__Fx_force = fx
        self.__Fy_force = fy 
        self.__Mz_force = mz
        self.__Type_force = type
        self.__Angle_force = angle
        
        # Fx
        # self.__Fx_x_beg = 0 
        # self.__Fx_y_beg = fx * l_/2 
        # self.__Fx_m_beg = 0
        
        # self.__Fx_x_end = 0 
        # self.__Fx_y_end = -fx * l_/2 
        # self.__Fx_m_end = 0
    
        # Fy
        if type == "GLOBAL":
            # angle_force_rad_ = math.radians(angle)
            # cos_force_ = math.cos(angle_force_rad_)
            # sin_force_ = math.sin(angle_force_rad_)
            
            self.__Fy_x_beg = 0 #fy * l_/2 * sin_barre_ * sin_force_
            self.__Fy_y_beg = fy * l_/2 #* cos_barre_ * cos_force_
            self.__Fy_m_beg = fy * l_*l_/12# * cos_barre_ * cos_force_
            
            self.__Fy_x_end = 0 #-fy * l_/2  * sin_barre_ * sin_force_
            self.__Fy_y_end = fy * l_/2# * cos_barre_ * cos_force_
            self.__Fy_m_end = -fy * l_*l_/12# * cos_barre_ * cos_force_
        else:
            self.__Fy_x_beg = fy * l_/2 
            self.__Fy_y_beg = fy * l_/2 
            self.__Fy_m_beg = fy * l_*l_/12
            
            self.__Fy_x_end = 0 
            self.__Fy_y_end = fy * l_/2 
            self.__Fy_m_end = -fy * l_*l_/12 
   
    def temperature(self, dT_x, dT_m):
        """ Function to define uniforme load on the barre

            :@param dT_x: thermal load in X axis
            :@param dT_m: thermal load in Z axis
            :@type dT_x: double
            :@type dT_m: double
        """

        self.__dT_x = True if dT_x != 0 else False
        self.__dT_m = True if dT_m != 0 else False
        
        self.__dT_force_x = dT_x
        self.__dT_force_m = dT_m

        if self.__Material == False and self.__Cross_section == False:
            E_ = 1
            Iy_ = 1
            alpha_ = 1
            h_ = 1
            A_ = 1
        else:
            E_ = self.__Material.E
            Iy_ = self.__Cross_section.Inertia_y
            A_ = self.__Cross_section.Area
            alpha_ = self.__Material.Alpha
            h_ = self.__Cross_section.H
            
        self.__dT_x_beg = E_*A_*alpha_*dT_x/self.__Length
        self.__dT_y_beg = 0
        self.__dT_m_beg = E_*Iy_*alpha_*dT_m/h_
        
        self.__dT_x_end = -E_*A_*alpha_*dT_x
        self.__dT_y_end = 0
        self.__dT_m_end = -E_*Iy_*alpha_*dT_m/h_

    def prestress_load(self, equation, kind = "RIVE", coef = [], prestress_value=1):
        """ Function to define prestress_load on the barre

            We considere that the equation is 2 polynomials
            
            M is define as P.ep(x)

            :@param equation: ep(x) equation
            :@param kind: position of the beam
            :@param coef: coefficient of the second degree equation
            :@param prestress_value: value of the prestress
            :@type equation: string
            :@type kind: string
            :@type coef: List
            :@type prestress_value: double
            :@default equation:          
            :@default kind: RIVE (or INTER)
            :@default coef: table  
            :@default prestress_value: 1 (to considere in function of th prestress)
        """

        self.__PC = True if prestress_value != 0 else False
        
        self.__PC_equation = equation
        self.__PC_value = prestress_value
        self.__PC_coef = coef
        self.__PC_kind = kind
        
        x_beg_ = self.__Pt_local_beg.X
        y_beg_ = self.__Pt_local_beg.Y

        x_end_ = self.__Pt_local_end.X
        y_end_ = self.__Pt_local_end.Y
        
        Length_ = math.sqrt((x_end_-x_beg_)**2 + (y_end_-y_beg_)**2)
        
        # print("local val")
        # print(self.__Pt_local_beg.X)
        # print(self.__Pt_local_end.X)
        # print("end")
        # print(self.__P_beg.X)
        # print(self.__P_end.X)
        # print("global")
        # print(Length_)
        # print("Length")
        
        if type(equation) == float or type(equation) == int:
            self.__PC_x_beg = -prestress_value
            self.__PC_y_beg = 0
            self.__PC_m_beg = prestress_value * equation

            self.__PC_x_end = -prestress_value
            self.__PC_y_end = 0
            self.__PC_m_end = -prestress_value * equation
  
        else: 
            if kind == "RIVE":
                L_alpha_L = coef[0] # (1-alpha)*L
                alpha_L = coef[1]
                
                X_beg = self.P_beg.X
                X_end = self.P_end.X
                
                if X_end > Length_:
                    X_beg -= self.__Pt_local_beg.X
                    X_end -= self.__Pt_local_beg.X

                if X_beg <= L_alpha_L:
                    a = equation[0][0]
                    b = equation[0][1]
                    c = equation[0][2]

                else:
                    a = equation[1][0]
                    b = equation[1][1]
                    c = equation[1][2]

                if X_end <= L_alpha_L:
                    a = equation[0][0]
                    b = equation[0][1]
                    c = equation[0][2]

                else:
                    a = equation[1][0]
                    b = equation[1][1]
                    c = equation[1][2]

                eq_beg = a*X_beg**2 + b*X_beg + c
                eq_end = a*X_end**2 + b*X_end + c
                
                # Beg
                f_a_beg = eq_beg
                f_p_a_beg = 2*a*eq_beg + b
                
                y_0_beg = f_a_beg + f_p_a_beg*(0-eq_beg)
                y_1_beg = f_a_beg + f_p_a_beg*(1-eq_beg)
                
                a_angle_beg = y_0_beg-y_1_beg
                b_angle_beg = 1
                
                angle_beg = math.atan(-a_angle_beg/b_angle_beg)

                #end
                f_a_end = eq_end
                f_p_a_end = 2*a*eq_end + b
                
                y_0_end = f_a_end + f_p_a_end*(0-eq_end)
                y_1_end = f_a_end + f_p_a_end*(1-eq_end)
                
                a_angle_end = y_0_end-y_1_end
                b_angle_end = 1
                
                angle_end = math.atan(-a_angle_end/b_angle_end)

            elif kind == "INTER":               
                beta_L = coef[0] # (1-alpha)*L
                L_beta_gamma_L = coef[1] # (1-beta-gamma)*L
                gamma_L = coef[2]

                X_beg = self.P_beg.X
                X_end = self.P_end.X

                X_beg -= self.__Pt_local_beg.X
                X_end -= self.__Pt_local_beg.X                    
            
                if X_beg <= beta_L:
                    a = equation[0][0]
                    b = equation[0][1]
                    c = equation[0][2]
                    
                elif X_beg <= (beta_L+L_beta_gamma_L):
                    a = equation[1][0]
                    b = equation[1][1]
                    c = equation[1][2]

                else:
                    a = equation[2][0]
                    b = equation[2][1]
                    c = equation[2][2]  

                if X_end <= beta_L:
                    a = equation[0][0]
                    b = equation[0][1]
                    c = equation[0][2]
                    
                elif X_end <= (beta_L+L_beta_gamma_L):
                    a = equation[1][0]
                    b = equation[1][1]
                    c = equation[1][2]

                else:
                    a = equation[2][0]
                    b = equation[2][1]
                    c = equation[2][2]   
                    
                    
                    
                eq_beg = a*X_beg**2 + b*X_beg + c
                eq_end = a*X_end**2 + b*X_end + c
                
                # Beg
                f_a_beg = eq_beg
                f_p_a_beg = 2*a*eq_beg + b
                
                y_0_beg = f_a_beg + f_p_a_beg*(0-eq_beg)
                y_1_beg = f_a_beg + f_p_a_beg*(1-eq_beg)
                
                a_angle_beg = y_0_beg-y_1_beg
                b_angle_beg = 1
                
                angle_beg = math.atan(-a_angle_beg/b_angle_beg)

                #end
                f_a_end = eq_end
                f_p_a_end = 2*a*eq_end + b
                
                y_0_end = f_a_end + f_p_a_end*(0-eq_end)
                y_1_end = f_a_end + f_p_a_end*(1-eq_end)
                
                a_angle_end = y_0_end-y_1_end
                b_angle_end = 1
                
                angle_end = math.atan(-a_angle_end/b_angle_end)
            
            self.__PC_x_beg = -prestress_value
            self.__PC_y_beg = 0
            self.__PC_m_beg = prestress_value * eq_beg * math.cos(angle_beg)

            self.__PC_x_end = -prestress_value
            self.__PC_y_end = 0
            self.__PC_m_end = -prestress_value * eq_end * math.cos(angle_end)  

# Special methode

    def __len__(self):
        return self.__length
    def __repr__(self):
        """ used when you print(Tbarre object) """
        if self.__NB_BARRE == 1:
            return "It exist {} element ".format(self.__NB_BARRE)
        else:
            return "It exist {} element".format(self.__NB_BARRE)
# Set
    def __set_section_property(self, val):
        self.__Cross_section = val  
    
    def __set_P_beg(self, val):
        self.__P_beg = val
    def __set_P_end(self, val):
        self.__P_end = val

    def __set_Pt_num_beg(self, val):
        self.__Pt_num_beg = val
    def __set_Pt_num_end(self, val):
        self.__Pt_num_end = val

    def __set_Pt_local_beg(self, val):
        self.__Pt_local_beg = val
    def __set_Pt_local_end(self, val):
        self.__Pt_local_end = val
       
    def __set_Fx_x_beg(self, val):
        self.__Fx_x_beg = val
    def __set_Fx_y_beg(self, val):
        self.__Fx_y_beg = val
    def __set_Fx_m_beg(self, val):
        self.__Fx_m_beg = val
        
    def __set_Fx_x_end(self, val):
        self.__Fx_x_end = val
    def __set_Fx_y_end(self, val):
        self.__Fx_y_end = val
    def __set_Fx_m_end(self, val):
        self.__Fx_m_end = val
        
    def __set_Fy_x_beg(self, val):
        self.__Fy_x_beg = val
    def __set_Fy_y_beg(self, val):
        self.__Fy_y_beg = val
    def __set_Fy_m_beg(self, val):
        self.__Fy_m_beg = val
        
    def __set_Fy_x_end(self, val):
        self.__Fy_x_end = val
    def __set_Fy_y_end(self, val):
        self.__Fy_y_end = val
    def __set_Fy_m_end(self, val):
        self.__Fy_m_end = val
        
    def __set_Mz_x_beg(self, val):
        self.__Mz_x_beg = val
    def __set_Mz_y_beg(self, val):
        self.__Mz_y_beg = val
    def __set_Mz_m_beg(self, val):
        self.__Mz_m_beg = val
        
    def __set_Mz_x_end(self, val):
        self.__Mz_x_end = val
    def __set_Mz_y_end(self, val):
        self.__Mz_y_end = val
    def __set_Mz_m_end(self, val):
        self.__Mz_m_end = val
        
    def __set_dT_x_beg(self, val):
        self.__dT_x_beg = val
    def __set_dT_y_beg(self, val):
        self.__dT_y_beg = val
    def __set_dT_m_beg(self, val):
        self.__dT_m_beg = val

    def __set_dT_x_end(self, val):
        self.__dT_x_end  = val
    def __set_dT_y_end(self, val):
        self.__dT_y_end = val
    def __set_dT_m_end(self, val):
        self.__dT_m_end = val
        
    def __set_PC_x_beg(self, val):
        self.__PC_x_beg  = val
    def __set_PC_y_beg(self, val):
        self.__PC_y_beg = val
    def __set_PC_m_beg(self, val):
        self.__PC_m_beg = val
 
    def __set_PC_x_end(self, val):
        self.__PC_x_end  = val
    def __set_PC_y_end(self, val):
        self.__PC_y_end = val
    def __set_PC_m_end(self, val):
        self.__PC_m_end = val
        
# Get
    def __get_Length(self):
        return self.__Length
    def __get_Angle(self):
        return self.__Angle
    def __get_Rot_mat(self):
        return self.__Rot_mat
    def __get_k_local_mat(self):
        return self.__k_local
    def __get_Name_p_beg(self):
        return self.__P_beg_name    
    def __get_Name_p_end(self):
        return self.__P_end_name
    def __get_k_barre_mat(self):
        return self.__K_barre
    def __get_Nb_barre(cls):
        return TBarre.__Nb_BARRE
    def __get_X_beg(self):
        return self.__P_beg.X
    def __get_Y_beg(self):
        return self.__P_beg.Y
    def __get_X_end(self):
        return self.__P_end.X
    def __get_Y_end(self):
        return self.__P_end.Y
    def __get_Pt_num_beg(self):
        return self.__Pt_num_beg
    def __get_Pt_num_end(self):
        return self.__Pt_num_end
 
    def __get_P_beg(self):
        return self.__P_beg
    def __get_P_end(self):
        return self.__P_end
  
    def __get_Pt_local_beg(self):
        return self.__Pt_local_beg
    def __get_Pt_local_end(self):
        return self.__Pt_local_end

    def __get_Fx_x_beg(self):
        return self.__Fx_x_beg
    def __get_Fx_y_beg(self):
        return self.__Fx_y_beg
    def __get_Fx_m_beg(self):
        return self.__Fx_m_beg
        
    def __get_Fx_x_end(self):
        return self.__Fx_x_end
    def __get_Fx_y_end(self):
        return self.__Fx_y_end
    def __get_Fx_m_end(self):
        return self.__Fx_m_end
        
    def __get_Fy_x_beg(self):
        return self.__Fy_x_beg
    def __get_Fy_y_beg(self):
        return self.__Fy_y_beg
    def __get_Fy_m_beg(self):
        return self.__Fy_m_beg
        
    def __get_Fy_x_end(self):
        return self.__Fy_x_end
    def __get_Fy_y_end(self):
        return self.__Fy_y_end
    def __get_Fy_m_end(self):
        return self.__Fy_m_end
        
    def __get_Mz_x_beg(self):
        return self.__Mz_x_beg
    def __get_Mz_y_beg(self):
        return self.__Mz_y_beg
    def __get_Mz_m_beg(self):
        return self.__Mz_m_beg
        
    def __get_Mz_x_end(self):
        return self.__Mz_x_end
    def __get_Mz_y_end(self):
        return self.__Mz_y_end
    def __get_Mz_m_end(self):
        return self.__Mz_m_end
        
    def __get_dT_x_beg(self):
        return self.__dT_x_beg
    def __get_dT_y_beg(self):
        return self.__dT_y_beg
    def __get_dT_m_beg(self):
        return self.__dT_m_beg

    def __get_dT_x_end(self):
        return self.__dT_x_end
    def __get_dT_y_end(self):
        return self.__dT_y_end
    def __get_dT_m_end(self):
        return self.__dT_m_end

    def __get_PC_x_beg(self):
        return self.__PC_x_beg
    def __get_PC_y_beg(self):
        return self.__PC_y_beg
    def __get_PC_m_beg(self):
        return self.__PC_m_beg 
 
    def __get_PC_x_end(self):
        return self.__PC_x_end
    def __get_PC_y_end(self):
        return self.__PC_y_end
    def __get_PC_m_end(self):
        return self.__PC_m_end

    def __get_Fx(self):
        return self.__Fx
    def __get_Fy(self):
        return self.__Fy
    def __get_Mz(self):
        return self.__Mz
    def __get_dT_x(self):
        return self.__dT_x
    def __get_dT_m(self):
        return self.__dT_m
    def __get_PC(self):
        return self.__PC
    
 # Property
 
    Length = property(__get_Length)
    Angle = property(__get_Angle)
    Rot_mat = property(__get_Rot_mat)
    K_local = property(__get_k_local_mat)
    
    P_beg = property(__get_P_beg, __set_P_beg)
    P_end = property(__get_P_end, __set_P_end)
    
    P_beg_name = property(__get_Name_p_beg)
    P_end_name = property(__get_Name_p_end)
    P_num_beg = property(__get_Pt_num_beg, __set_Pt_num_beg)
    P_num_end = property(__get_Pt_num_end, __set_Pt_num_end)
 
    Pt_local_beg = property(__get_Pt_local_beg, __set_Pt_local_beg)
    Pt_local_end = property(__get_Pt_local_end, __set_Pt_local_end)

    K_barre = property(__get_k_barre_mat)
    
    Cross_section = property(None,__set_section_property)
    
    X_beg = property(__get_X_beg)
    Y_beg = property(__get_Y_beg)
    X_end = property(__get_X_end)
    Y_end = property(__get_Y_end)

    Fx_x_beg = property(__get_Fx_x_beg, __set_Fx_x_beg)
    Fx_y_beg = property(__get_Fx_y_beg, __set_Fx_y_beg)
    Fx_m_beg = property(__get_Fx_m_beg, __set_Fx_m_beg)

    Fx_x_end = property(__get_Fx_x_end, __set_Fx_x_end)
    Fx_y_end = property(__get_Fx_y_end, __set_Fx_y_end)
    Fx_m_end = property(__get_Fx_m_end, __set_Fx_m_end)
  
    Fy_x_beg = property(__get_Fy_x_beg, __set_Fy_x_beg)
    Fy_y_beg = property(__get_Fy_y_beg, __set_Fy_y_beg)
    Fy_m_beg = property(__get_Fy_m_beg, __set_Fy_m_beg)

    Fy_x_end = property(__get_Fy_x_end, __set_Fy_x_end)
    Fy_y_end = property(__get_Fy_y_end, __set_Fy_y_end)
    Fy_m_end = property(__get_Fy_m_end, __set_Fy_m_end)
    
    Mz_x_beg = property(__get_Mz_x_beg, __set_Mz_x_beg)
    Mz_y_beg = property(__get_Mz_y_beg, __set_Mz_y_beg)
    Mz_m_beg = property(__get_Mz_m_beg, __set_Mz_m_beg)

    Mz_x_end = property(__get_Mz_x_end, __set_Mz_x_end)
    Mz_y_end = property(__get_Mz_y_end, __set_Mz_y_end)
    Mz_m_end = property(__get_Mz_m_end, __set_Mz_m_end)

    dT_x_beg = property(__get_dT_x_beg, __set_dT_x_beg)
    dT_y_beg = property(__get_dT_y_beg, __set_dT_y_beg)
    dT_m_beg = property(__get_dT_m_beg, __set_dT_m_beg)

    dT_x_end = property(__get_dT_x_end, __set_dT_x_end)
    dT_y_end = property(__get_dT_y_end, __set_dT_y_end)
    dT_m_end = property(__get_dT_m_end, __set_dT_m_end)
    
    PC_x_beg = property(__get_PC_x_beg, __set_PC_x_beg)
    PC_y_beg = property(__get_PC_y_beg, __set_PC_y_beg)
    PC_m_beg = property(__get_PC_m_beg, __set_PC_m_beg)

    PC_x_end = property(__get_PC_x_end, __set_PC_x_end)
    PC_y_end = property(__get_PC_y_end, __set_PC_y_end)
    PC_m_end = property(__get_PC_m_end, __set_PC_m_end)
    
    Fx = property(__get_Fx)
    Fy = property(__get_Fy)
    Mz = property(__get_Mz)
    dT_x = property(__get_dT_x)
    dT_m = property(__get_dT_m)
    PC = property(__get_PC)

class TStiffness_methode:
    """
        Class to do calculation
        
        This class can be define a "symbolic class"
        it's mean that all calculation will be algerbric

        :@param __INTERVAL_POINT: 
        :@param __SUM_EQ: 
        :@type __INTERVAL_POINT: integer
        :@type __SUM_EQ: integer
        :@default __INTERVAL_POINT: 50 (Number of point between two node to make graphic)
        :@default __SUM_EQ: 3 (Number of equation by node)
    """
 # Attribute
    __INTERVAL_POINT = 50
    __SUM_EQ = 3

    def __init__(self, barre_array, point_array, symbolic=False):
        """ Constructor
            :@param barre_array: tuple of all barre
            :@param point_array: tuple of all point
            :@param symbolic: Choose if all calculation will be algerbric
            :@type barre_array: tuple
            :@type point_array: tuple
            :@type symbolic: bool
        """
        
        self.__Barre_tab = barre_array
        self.__Point_tab = point_array    
        
        # Lintel variable
        
        self.__a = 0
        self.__b = 0
        
        # Calculation
        self.routine_calculation()

    def routine_calculation(self):
        """ Function to make and remake all calculaion """
        
        # Define element
        start = timeit.default_timer()
        self.__define_Support_tab()
        self.__define_D_tab()
        self.__define_Force_tab()
        print("     Définition des éléments: " + str(timeit.default_timer()-start))
        
        # Define matrix         
        start = timeit.default_timer()
        self.__define_connection_table()
        print("     Définition des la tables des connexions: " + str(timeit.default_timer()-start))   
        start = timeit.default_timer()        
        self.__define_global_stiffness_mat()
        print("     Définition de la mat global: " + str(timeit.default_timer()-start)) 
        # Calculation
        start = timeit.default_timer()
        self.__mat_modif()
        print("     Modification de la matrice: " + str(timeit.default_timer()-start)) 
        
        start = timeit.default_timer()
        self.__calc_D_Rint()
        print("     Calcul des resultats: " + str(timeit.default_timer()-start)) 
        
        start = timeit.default_timer()
        self.__fill_point()
        print("     Ecriture des données dans points: " + str(timeit.default_timer()-start)) 
        start = timeit.default_timer()
        self.__interne_force()
        print("     Définition des forces internes: " + str(timeit.default_timer()-start)) 
        start = timeit.default_timer()
        self.__write_interal_force()
        print("     Ecriture des forces internes: " + str(timeit.default_timer()-start)) 

    def __define_Support_tab(self):
        """ Function to fill support matrix 
            __Support_tab  = [Rax, Ray, M]
            1 mean reaction existe
            0 mean reaction doesn't existe
        """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__Support_tab = np.zeros(point) #1,point)
        counter_ = 0

        for i in self.__Point_tab:
            self.__Support_tab[counter_] = 1 if i.Rx_cond == True else 0
            self.__Support_tab[counter_+1] = 1 if i.Ry_cond == True else 0
            self.__Support_tab[counter_+2] = 1 if i.Mt_cond == True else 0
            counter_ += 3

    def __define_D_tab(self):
        """ Function to fill displacement tab
            __D_tab  = [dx, dy, theta]
            1 mean displacement existe
            0 mean displacement doesn't existe
        """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__D_tab = np.zeros(point) # 1, point)
    
        self.__Sum_int = 0 # sum of unknown reaction
        
        for i in range(0,point):
            if self.__Support_tab[i] == 1:
                self.__D_tab[i] = 0
                self.__Sum_int += 1
            else:
                self.__D_tab[i] = 1

    def __define_Force_tab(self):
        """ Function to fill force tab
            __Force_tab  = [Fx, Fy, Mt]
        """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__Force_tab = np.zeros(point)#(1,point)
        counter_ = 0
        barre_done_ = []

        for i in self.__Point_tab:
            self.__Force_tab[counter_] = i.Fx
            self.__Force_tab[counter_+1] = i.Fy
            self.__Force_tab[counter_+2] = i.Mz

            if TBarre.NB_BARRE != 1:
                for ii in self.__Barre_tab:
                    if (ii.Fx or ii.Fy or ii.Mz or ii.dT_x or ii.dT_m or ii.PC):
                        if i.Name == ii.P_beg_name:
                            self.__Force_tab[counter_] += ii.Fx_x_beg  \
                                                + ii.Fy_x_beg + ii.Mz_x_beg \
                                                + ii.dT_x_beg + ii.PC_x_beg
                            self.__Force_tab[counter_+1] += ii.Fx_y_beg \
                                                + ii.Fy_y_beg + ii.Mz_y_beg \
                                                + ii.dT_y_beg + ii.PC_y_beg
                            self.__Force_tab[counter_+2] += ii.Fx_m_beg \
                                                + ii.Fy_m_beg + ii.Mz_m_beg \
                                                + ii.dT_m_beg + ii.PC_m_beg
                        elif i.Name == ii.P_end_name:
                            self.__Force_tab[counter_] += ii.Fx_x_end \
                                                + ii.Fy_x_end + ii.Mz_x_end \
                                                + ii.dT_x_end + ii.PC_x_end
                            self.__Force_tab[counter_+1] += ii.Fx_y_end \
                                                + ii.Fy_y_end + ii.Mz_y_end \
                                                + ii.dT_y_end + ii.PC_y_end
                            self.__Force_tab[counter_+2] += ii.Fx_m_end \
                                                + ii.Fy_m_end + ii.Mz_m_end \
                                                + ii.dT_m_end + ii.PC_m_end
            else:
                ii = self.__Barre_tab
                if (ii.Fx or ii.Fy or ii.Mz or ii.dT_x or ii.dT_m or ii.PC):
                    if i.Name == ii.P_beg_name:
                        self.__Force_tab[counter_] += ii.Fx_x_beg  \
                                            + ii.Fy_x_beg + ii.Mz_x_beg \
                                            + ii.dT_x_beg + ii.PC_x_beg
                        self.__Force_tab[counter_+1] += ii.Fx_y_beg \
                                            + ii.Fy_y_beg + ii.Mz_y_beg \
                                            + ii.dT_y_beg + ii.PC_y_beg
                        self.__Force_tab[counter_+2] += ii.Fx_m_beg \
                                            + ii.Fy_m_beg + ii.Mz_m_beg \
                                            +  ii.dT_m_beg + ii.PC_m_beg
                    elif i.Name == ii.P_end_name:
                        self.__Force_tab[counter_] += ii.Fx_x_end \
                                            + ii.Fy_x_end + ii.Mz_x_end \
                                            + ii.dT_x_end + ii.PC_x_end
                        self.__Force_tab[counter_+1] += ii.Fx_y_end \
                                            + ii.Fy_y_end + ii.Mz_y_end \
                                            + ii.dT_y_end + ii.PC_y_end
                        self.__Force_tab[counter_+2] += ii.Fx_m_end \
                                            + ii.Fy_m_end + ii.Mz_m_end \
                                            + ii.dT_m_end + ii.PC_m_end
            counter_ += 3

    def __define_connection_table(self):
        """ Function the connection table
        
            The connection table to create stiffness matrix
            
            pt_1(0,0); pt_2(0,1); pt_3(1,1); pt_4(1,0)
            b1(pt_1,pt_2); b2(pt_2,pt_3); b3(pt_3,pt_4)
            
                pt_1 | pt_2 | pt_3 | pt_4 |
            b1 |  x  |   x  |   -  |   -  |
            b2 |  -  |   x  |   x  |   -  |
            b3 |  -  |   -  |   x  |   x  |
        """
        col_ = len(self.__Point_tab)
        row_ = TBarre.NB_BARRE

        row_b_ = 0
        self.__Connect_tab = np.zeros((row_, col_))
        if TBarre.NB_BARRE != 1:
            for barre in self.__Barre_tab:
                col_b_ = 0
                for point in self.__Point_tab:
                    if barre.P_beg_name == point.Name or barre.P_end_name == point.Name:
                        self.__Connect_tab[row_b_, col_b_] = 1 
                    else:
                        self.__Connect_tab[row_b_, col_b_] = 0
                    col_b_ += 1
                row_b_ += 1
        else:
            col_b_ = 0
            barre = self.__Barre_tab
            for point in self.__Point_tab:
                if barre.P_beg_name == point.Name or barre.P_end_name == point.Name:
                    self.__Connect_tab[row_b_, col_b_] = 1
                else:
                    self.__Connect_tab[row_b_, col_b_] = 0
                col_b_ += 1
            row_b_ += 1

    def __define_global_stiffness_mat(self):
        """ Function to mix the global stifness matrix """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__K_global = np.zeros((point, point), dtype=float)
        pass_ = np.zeros(TBarre.NB_BARRE) #1,TBarre.NB_BARRE)
                
        for i in range(0,TPoint.NB_POINT * 3,3):
            for ii in range(0,TPoint.NB_POINT * 3,3):
                for iii in range(0,TBarre.NB_BARRE):
                    if TBarre.NB_BARRE != 1:
                        my_tab = self.__Barre_tab[iii].K_barre
                    else:
                        my_tab = self.__Barre_tab.K_barre
                
                    if self.__Connect_tab[iii, int(i / 3)] != 0 and self.__Connect_tab[iii, int(ii / 3)] != 0:
                        if i == 0 and ii == 0: # k11
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.__K_global[j, jj] += self.__Connect_tab[iii, int(ii / 3)] * self.__Connect_tab[iii, int(i / 3)] * my_tab[j - i , jj - ii]
                            pass_[iii] = 1
                        elif i == ii: # k11 + k22
                            if pass_[iii] == 1:
                                for j in range(i, i + 3):
                                    for jj in range(ii, ii + 3):
                                        self.__K_global[j, jj] += self.__Connect_tab[iii, int(ii / 3)] * self.__Connect_tab[iii, int(i / 3)] * my_tab[j - i  + 3, jj - ii  + 3]
                            else:
                                for j in range(i, i + 3):
                                    for jj in range(ii, ii + 3):
                                        self.__K_global[j, jj] += self.__Connect_tab[iii, int(i / 3)] * self.__Connect_tab[iii, int(i / 3)] * my_tab[j - i , jj - ii ]
                                pass_[iii] = 1
                        elif i + 3 == ii: # k12
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.__K_global[j, jj] += + self.__Connect_tab[iii, int(ii / 3)] * self.__Connect_tab[iii, int(i / 3)] * my_tab[j - i , jj - ii + 3 ]
                        elif i == ii + 3: # k21 
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.__K_global[j, jj] += self.__Connect_tab[iii, int(ii / 3)] * self.__Connect_tab[iii, int(i / 3)] * my_tab[j - i + 3 , jj - ii ] 

    def __mat_modif(self):
        """ Multiply k_global by D_tab
            Removing zero form D_tab
        """

        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        kxd_ = np.zeros( (point, point) ,dtype=float)
        k_d_wz_ = np.zeros( (point, point), dtype=float)
        b = 0
        pass_ = False
        
        for i in range(0,point): # Row
            a = 0
            for ii in range(0,point): # Col
                kxd_[ii,i] = self.__K_global[i, ii] * self.__D_tab[i]              
                if self.__D_tab[i] != 0:
                    k_d_wz_[a,b] = kxd_[ii,i]
                    a += 1
                    pass_ = True
            if pass_:
                b += 1
                pass_ = False
        
        self.k_d_wz_r_ = k_d_wz_
        
        
        a = point-1
        
        for i in range(point-1,-1,-1):
            if self.__Support_tab[i] != 0:
                for ii in range(point-1,-1,-1):
                    if ii == i:
                        self.k_d_wz_r_[ii,a] = -1
                a -= 1

    def __calc_D_Rint(self):
        """ Calculate the matrix of displacement
            and support reaction
            
            Support reaction will alway be at the end_type_
            [dx, dy, rx, ry]
        """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__Unds_tab = np.zeros(point)#1,point)
        
        start = timeit.default_timer()
        mat_inverse_ = np.linalg.inv(self.k_d_wz_r_) # Matrix inversion
        print("         Inversion de la matrice de rigidité: " + str(timeit.default_timer()-start)) 
        self.__Unds_tab =  np.matmul(mat_inverse_, self.__Force_tab)
        
    def __fill_point(self):
        """ fill reaction in point
            fill displacement in point
        """
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        self.__Delta_theta_str = np.zeros(point) # 1,point)
        a = 0
        b = 0
        
        pass_ = 0
        for i in range(0, point):
            if self.__Support_tab[i] == 1:
                if i%3 == 0:
                    self.__Point_tab[int(i/3)].Rx = self.__Unds_tab[point - self.__Sum_int + a]
                elif i%3 == 1:
                    self.__Point_tab[int((i-1)/3)].Ry = self.__Unds_tab[point - self.__Sum_int + a]
                elif i%3 == 2:
                    self.__Point_tab[int((i-2)/3)].Mt = self.__Unds_tab[point - self.__Sum_int + a]
                a += 1
      
            if self.__D_tab[i] == 1:
                if i%3 == 0:
                    self.__Point_tab[int(i/3)].Delta_x = self.__Unds_tab[b]
                elif i%3 == 1:
                    self.__Point_tab[int((i-1)/3)].Delta_y = self.__Unds_tab[b]
                elif i%3 == 2:
                    self.__Point_tab[int((i-1)/3)].Theta = self.__Unds_tab[b]
                self.__Delta_theta_str[i] = self.__Unds_tab[b]
                b += 1
            else:
                if i%3 == 0:
                    self.__Point_tab[int(i/3)].Delta_x = 0
                elif i%3 == 1:
                    self.__Point_tab[int((i-1)/3)].Delta_y = 0
                elif i%3 == 2:
                    self.__Point_tab[int((i-2)/3)].Theta = 0
                self.__Delta_theta_str[i] = 0

    def __interne_force(self):
        """ calculate internal force 
            fill in odered fonction of node
        """
        
        point = TPoint.NB_POINT * self.__SUM_EQ #  Number of point
        tmp_delta_ = np.zeros(self.__SUM_EQ*2) #,1)
       
        self.__NSM_effort = np.zeros(point) #1,point)
        
        if TBarre.NB_BARRE != 1:
            for i in self.__Barre_tab:
                for ii in range(0,3):

                    tmp_delta_[ii] = self.__Delta_theta_str[i.P_num_beg *3 +ii-3]
                    tmp_delta_[ii+3] = self.__Delta_theta_str[i.P_num_end *3 +ii-3]
                
                tmp_ = np.matmul(i.K_local, i.Rot_mat)
                NSM_tmp_ = np.matmul(tmp_, tmp_delta_)
                
                for ii in range(0,3):
                    if ii == 0: # Fx
                        add_beg_ = i.Fx_x_beg + i.Fy_x_beg + i.Mz_x_beg + i.dT_x_beg + i.PC_x_beg  
                        add_end_ = i.Fx_x_end + i.Fy_x_end + i.Mz_x_end + i.dT_x_end + i.PC_x_end                       
                    elif ii == 1: # Fy
                        add_beg_ = i.Fx_y_beg + i.Fy_y_beg + i.Mz_y_beg + i.dT_y_beg + i.PC_y_beg    
                        add_end_ = i.Fx_y_end + i.Fy_y_end + i.Mz_y_end + i.dT_y_end + i.PC_y_end
                    elif ii == 2: # Mz
                            add_beg_ = i.Fx_m_beg + i.Fy_m_beg + i.Mz_m_beg + i.dT_m_beg + i.PC_m_beg     
                            add_end_ = i.Fx_m_end + i.Fy_m_end + i.Mz_m_end + i.dT_m_end + i.PC_m_end 
                    self.__NSM_effort[i.P_num_beg*3+ii-3] = NSM_tmp_[ii]  - add_beg_
                    self.__NSM_effort[i.P_num_end*3+ii-3] = -NSM_tmp_[ii+3]  + add_end_
        else:
            i = self.__Barre_tab
            for ii in range(0,3):

                tmp_delta_[ii] = self.__Delta_theta_str[i.P_num_beg *3 +ii-3] 
                tmp_delta_[ii+3] = self.__Delta_theta_str[i.P_num_end *3 +ii-3] 

            tmp_ = np.matmul(i.K_local, i.Rot_mat)
            NSM_tmp_ = np.matmul(tmp_, tmp_delta_)
            
            for ii in range(0,3):
                if ii == 0: # Fx
                    add_beg_ = i.Fx_x_beg + i.Fy_x_beg + i.Mz_x_beg + i.dT_x_beg + i.PC_x_beg  
                    add_end_ = i.Fx_x_end + i.Fy_x_end + i.Mz_x_end + i.dT_x_end + i.PC_x_end                       
                elif ii == 1: # Fy
                    add_beg_ = i.Fx_y_beg + i.Fy_y_beg + i.Mz_y_beg + i.dT_y_beg + i.PC_y_beg    
                    add_end_ = i.Fx_y_end + i.Fy_y_end + i.Mz_y_end + i.dT_y_end + i.PC_y_end
                elif ii == 2: # Mz
                        add_beg_ = i.Fx_m_beg + i.Fy_m_beg + i.Mz_m_beg + i.dT_m_beg + i.PC_m_beg     
                        add_end_ = i.Fx_m_end + i.Fy_m_end + i.Mz_m_end + i.dT_m_end + i.PC_m_end 

                self.__NSM_effort[i.P_num_beg*3+ii-3] = NSM_tmp_[1,ii] - add_beg_
                self.__NSM_effort[i.P_num_end*3+ii-3] = NSM_tmp_[1,ii+3] + add_end_
             
    def __write_interal_force(self):
        """ fill force in point """
        
        ii = 0
        
        for i in self.__Point_tab:
            i.define_internal_force(self.__NSM_effort[ii], self.__NSM_effort[ii+1],self.__NSM_effort[ii+2])
            ii += 3
            
    @classmethod
    def test_iso(cls, point_array):
        """
            Function to know the hyperstaticity of the structure
            @parma point_array: List of all point
            @type point_array: tuple
            
            @param return: Hypostatic; Isostatique; Hyperstatic
            @type return: String
        """
        counter_ = 0
        for pt in point_array:
            counter_ += pt.Hyper_degree
        if counter_-3 < 0:
            return "Hypostatic"
        elif counter_-3 == 0:
            return "Isostatique"
        else:
            return "Hyperstatic"

# Set
    def __set_Interval_point(self,val):
        self.__INTERVAL_POINT = val
    def __set_Sum_eq(self, val):
        self.__SUM_EQ = val
    def __set_a(self, var):
        self.__a = var
    def __set_b(self, var):
        self.__b = var
    def __set_Point(self, var):
        self.__Point_tab = var
    def __set_Barre(self, var):
        self.__Barre_tab = var
    
# Get
    def __get_K_global(self):
        return self.__K_global
    def __get_Interval_point(self):
        return self.__INTERVAL_POINT
    def __get_Sum_eq(self):
        return self.__SUM_EQ
    def __get_Support_tab(self):
        return self.__Support_tab
    def __get_D_tab(self):
        return self.__D_tab
    def __get_Force_tab(self):
        return self.__Force_tab
    def __get_Unds_tab(self):
        return self.__Unds_tab
    def __get_a(self):
        return self.__a 
    def __get_b(self):
        return self.__b
    def __get_Connect_tab(self):
        return self.__Connect_tab

 # Property
    INTERVAL_POINT = property(__get_Interval_point, __set_Interval_point)
    SUM_EQ = property(__set_Sum_eq, __get_Sum_eq)
    K_global = property(__get_K_global)
    Support_tab = property(__get_Support_tab)
    D_tab = property(__get_D_tab)
    Force_tab = property(__get_Force_tab)
    Unds_tab = property(__get_Unds_tab)
    Connect_tab = property(__get_Connect_tab)
    
    a = property(__get_a,__set_a)
    b = property(__get_b,__set_b)
    
    Point = property(None, __set_Point)
    Barre = property(None, __set_Barre)
    

class TSplit:
    """
        this class is for splitting the barre
    """

    def __init__(self, P_beg, P_end, Barre, step, point_all, barre_all):
        """
           Constructor
           
            :@type P_beg: 
        """
        self.__Step = step
        self.__Point = []
        self.__Barre = []
        
        self.__Point_all = point_all
        self.__Barre_all = barre_all
        
        self.__Barre_lmt = Barre
        
        self.__Pt_beg = P_beg
        self.__Pt_end = P_end
        
        self.__Pt_beg_Name = P_beg.Name
        self.__Pt_end_Name = P_end.Name
        
        self.__Pt_X_beg = P_beg.X
        self.__Pt_X_end = P_end.X

        self.__Pt_Y_beg = P_beg.Y
        self.__Pt_Y_end = P_end.Y
        
        start = timeit.default_timer()
        self.__devide_point()
        print("     Division des points: " + str(timeit.default_timer()-start))
        start = timeit.default_timer()
        self.__devide_barre()
        print("     Division des barres: " + str(timeit.default_timer()-start))
        start = timeit.default_timer()
        self.__rename_elmt()
        print("     Renumerotation: " + str(timeit.default_timer()-start))
        print("\n")
    
    def __devide_point(self):
        """
            function
        """
        
        if self.__Pt_Y_beg == 0 and self.__Pt_Y_end == 0:
            
            counter_ = 0
            Length_ = abs(self.__Pt_X_beg - self.__Pt_X_end)
            step_tab_ = np.arange(0.0, (Length_+Length_/self.__Step), Length_/self.__Step)
            step_name_ = Length_*Length_/self.__Step
            Name_ = self.__Pt_beg_Name+self.__Pt_end_Name
            
            value_name = step_name_

            for i in step_tab_:
                
                if i != 0 and i != Length_:
                    X_ = self.__Pt_X_beg  
                    new_name_ = Name_
                    point_ = TPoint(X_+i,0,new_name_ + " " + str(value_name))
                    self.__Point.append(point_)
                    value_name += step_name_

                elif i == 0:
                    self.__Point.append(self.__Pt_beg)
                elif i == Length_:
                    self.__Point.append(self.__Pt_end)  
                counter_ += 1

    def __devide_barre(self):
        """
            Function
        """
        if self.__Pt_Y_beg == 0 and self.__Pt_Y_end == 0:
            
            Length_ = abs(self.__Pt_X_beg - self.__Pt_X_end)
            beg_ = True
            step_tab_ = np.arange(0.0, (Length_+Length_/self.__Step), Length_/self.__Step)
            
            length_ = len(self.__Point)
            
            counter_ = 0

            for i in range(0, length_-1):
                
                tmp_barre = copy.copy(self.__Barre_lmt)

                self.__Barre.append(tmp_barre)
                self.__Barre[counter_].P_beg = self.__Point[i]
                self.__Barre[counter_].P_end = self.__Point[i+1]
                self.__Barre[counter_].Pt_local_beg = self.__Barre_lmt.P_beg
                self.__Barre[counter_].Pt_local_end = self.__Barre_lmt.P_end
                self.__Barre[counter_].define_property()  
                self.__Barre[counter_].redefine_force()
 
                counter_ += 1
            TBarre.NB_BARRE +=  counter_ - 1         

    def __rename_elmt(self):
        Barre_tmp = []
        Point_tmp = []
        try:
            Length_ = len(self.__Barre_all)
        except:
            Length_ = 1
        pass_ = False
        counter_ = 0

        if Length_ != 1:
            for i in range(0,Length_):
                if self.__Barre_all[i] == self.__Barre_lmt:
                    for ii in self.__Barre:
                        if counter_ == 0:
                            if i == 0:
                                self.__Point[0].Pt_num = 1
                                self.__Point[1].Pt_num = 2
                                
                                Point_tmp.append(self.__Point[0])
                                Point_tmp.append(self.__Point[1])
                                
                                ii.P_num_beg = 1
                                ii.P_num_end = 2
                                Barre_tmp.append(ii)
                            else:
                                P_beg_num = self.__Barre_all[i].P_num_beg                           
                                P_end_num = P_beg_num + 1
                                self.__Point[counter_+1].Pt_num = P_end_num
                                
                                Point_tmp.append(self.__Point[counter_+1])
                                
                                ii.P_num_end = P_end_num
                                Barre_tmp.append(ii)
                        else:
                            P_beg_num = Barre_tmp[i+counter_-1].P_num_end
                            P_end_num = P_beg_num + 1
                            
                            self.__Point[counter_+2-1].Pt_num = P_end_num
                            
                            Point_tmp.append(self.__Point[counter_+2-1])
                            
                            ii.P_num_beg = P_beg_num                        
                            ii.P_num_end = P_end_num
                            Barre_tmp.append(ii)
                        
                        counter_ += 1
                    pass_ = True
                
                elif pass_ == True:
                    P_beg_num = Barre_tmp[i+counter_-1-1].P_num_end
                    P_end_num = P_beg_num + 1


                    self.__Barre_all[i].P_num_beg = P_beg_num                        
                    self.__Barre_all[i].P_num_end = P_end_num
                         
                    self.__Barre_all[i].P_end.Pt_num = P_end_num
                    
                    Point_tmp.append(self.__Barre_all[i].P_end)
                            
                    Barre_tmp.append(self.__Barre_all[i])

                elif pass_ == False:
                    if i == 0:
                        Point_tmp.append(self.__Barre_all[i].P_beg)
                        Point_tmp.append(self.__Barre_all[i].P_end)
                        Barre_tmp.append(self.__Barre_all[i])
                    else:
                        Point_tmp.append(self.__Barre_all[i].P_end)
                        Barre_tmp.append(self.__Barre_all[i])
        else:
            for ii in self.__Barre:
                if counter_ == 0:
                    self.__Point[0].Pt_num = 1
                    self.__Point[1].Pt_num = 2
                    
                    Point_tmp.append(self.__Point[0])
                    Point_tmp.append(self.__Point[1])
                    
                    ii.P_num_beg = 1
                    ii.P_num_end = 2
                    Barre_tmp.append(ii)
                else:
                    P_beg_num = Barre_tmp[counter_-1].P_num_end
                    P_end_num = P_beg_num + 1
                    
                    self.__Point[counter_+2-1].Pt_num = P_end_num
                    
                    Point_tmp.append(self.__Point[counter_+2-1])
                    
                    ii.P_num_beg = P_beg_num                        
                    ii.P_num_end = P_end_num
                    Barre_tmp.append(ii)
                
                counter_ += 1
        
        self.__Barre = Barre_tmp
        self.__Point = Point_tmp
# Get

    def __get_Point(self):
        return self.__Point
    def __get_Barre(self):
        return self.__Barre
        
    Point = property(__get_Point)
    Barre = property(__get_Barre)

if __name__ == "__main__":    
    
   # start = timeit.default_timer()

   # my_sec = sec.TCustom()
   # my_sec.Area = 11.333 # m2
   # my_sec.Inertia_y = 25.5375 # m4
   # my_sec.H = 4.2 # m
    
   # my_mat = mat.TMaterial()
    
   # my_mat.E = 35000 # MPa 
    #my_mat.Alpha = 10 * 10**(-6)
    
    P1 = TPoint(0,0)
    P2 = TPoint(50,0)
    P3 = TPoint(110,0)
    P4 = TPoint(170,0)
    P5 = TPoint(230,0)
    P6 = TPoint(290,0)
    P7 = TPoint(340,0)
    
    P1.define_support_condition(True,True,False)
    P2.define_support_condition(True,True,False)
    P3.define_support_condition(True,True,False)
    P4.define_support_condition(True,True,False)
    P5.define_support_condition(True,True,False)
    P6.define_support_condition(True,True,False)
    P7.define_support_condition(True,True,False)
    
    B1 = TBarre(P1, P2)  #, my_sec, my_mat)
    B2 = TBarre(P2, P3)#, my_sec, my_mat)
    B3 = TBarre(P3, P4)#, my_sec, my_mat)
    B4 = TBarre(P4, P5)#, my_sec, my_mat)
    B5 = TBarre(P5, P6)#, my_sec, my_mat)
    B6 = TBarre(P6, P7)#, my_sec, my_mat)

    
    super = 3.5  # MN/m
   # Pp = 25 * my_sec.Area / 1000 # MN/m
    UDL = 48.9 /1000 # MN/m

    Value_uniforme = - UDL
    

    B1.uniforme_load(0,Value_uniforme,0)
    B2.uniforme_load(0,Value_uniforme,0)
    B3.uniforme_load(0,Value_uniforme,0)
    B4.uniforme_load(0,Value_uniforme,0)
    B5.uniforme_load(0,Value_uniforme,0)
    B6.uniforme_load(0,Value_uniforme,0)


    # dT = 12
    
    # B1.temperature(0,dT)
    # B2.temperature(0,dT)
    # B3.temperature(0,dT)
    # B4.temperature(0,dT)
    # B5.temperature(0,dT)
    # B6.temperature(0,dT)

    # eq_1 = ([.005984, -.23934, 0],
            # [-0.015666,  1.566, - 35.085 - 2.51])
    
    # eq_2 = ([-0.010879, 0, 4.08 - 2.51],
            # [0.007387, -.443222, 6.768333 - 2.51],
            # [-0.010879, 1.3055, - 35.085 - 2.51])

    # eq_3 = ([-0.15666, 0, + 4.08 - 2.51],
            # [0.005984, -0.359010, + 5.505150 - 2.51])
     
    # B1.prestress_load(eq_1, "RIVE", [40,10])
    # B2.prestress_load(eq_2, "INTER", [12,36,12])  
    # B3.prestress_load(eq_2, "INTER", [12,36,12])
    # B4.prestress_load(eq_2, "INTER", [12,36,12])
    # B5.prestress_load(eq_2, "INTER", [12,36,12])
    # B6.prestress_load(eq_3, "RIVE", [10,40])

    
    point = (P1, P2, P3, P4, P5, P6, P7)
    barre = (B1, B2, B3, B4, B5, B6) 

    # IL_itrerative(point, barre, (0,- UDL,0), "UNI", 100)
    
    print("Mise en place des données: " + str(timeit.default_timer()-start))

    start = timeit.default_timer()
    start_2 = timeit.default_timer()
    nb_devid = 20

    my_eltm = TSplit(P1, P2, B1, nb_devid, point, barre)
    
    point = my_eltm.Point
    barre = my_eltm.Barre
    
    print("Division d'un élément: " + str(timeit.default_timer()-start))
    print("\n")
    
    my_eltm = TSplit(P2, P3, B2, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre
    
    my_eltm = TSplit(P3, P4, B3, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = TSplit(P4, P5, B4, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = TSplit(P5, P6, B5, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = TSplit(P6, P7, B6, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre
    
    # os.system("pause")
    
    print("Division de tous les éléments: " + str(timeit.default_timer()-start_2))
  
    print("\n")
    print("Lancement des calculs:")
    start = timeit.default_timer()
    print(" Nb de point: " + str(len(point)))
    print(" Nb de barre: " + str(len(barre)))
    result = TStiffness_methode(barre, point)

    print("Fin du calcul: " + str(timeit.default_timer()-start))
    
    # start = timeit.default_timer()
    # """
    import matplotlib.pyplot as plt
    # import xlwings as xw
    X = []
    Moment = []
    Shear = []
    Normal = []
    for i in point:
        X.append(i.X)
        Moment.append(i.Moment)
        Shear.append(i.Shear)
        Normal.append(i.Normal)

   # wb = xw.Book('Charge.xlsx')
    
 #   worksheet_name = 'dT>0'
    
    max = len(Moment)
    
#    for i in range(0,max):
        
 #       if i == 0:
#            wb.sheets[worksheet_name].range((1,1)).value = "Abscisse X"
 #           wb.sheets[worksheet_name].range((1,2)).value = "Effort Normal" # row, col
#            wb.sheets[worksheet_name].range((1,3)).value = "Effort Tranchant" 
#            wb.sheets[worksheet_name].range((1,4)).value = "Moment" 

#        wb.sheets[worksheet_name].range((2+i,1)).value = X[i]
#        wb.sheets[worksheet_name].range((2+i,2)).value = Normal[i] # row, col
#        wb.sheets[worksheet_name].range((2+i,3)).value = Shear[i] 
#        wb.sheets[worksheet_name].range((2+i,4)).value = Moment[i]


    # nb = 6
    
    # for i in range(0,max):
        
        # if i == 0:
            # wb.sheets[worksheet_name].range((1,1+(nb-1)*5)).value = "Travée " + str(nb)          
            # wb.sheets[worksheet_name].range((2,1+(nb-1)*5)).value = "Abscisse X"
            # wb.sheets[worksheet_name].range((2,2+(nb-1)*5)).value = "Effort Normal" # row, col
            # wb.sheets[worksheet_name].range((2,3+(nb-1)*5)).value = "Effort Tranchant" 
            # wb.sheets[worksheet_name].range((2,4+(nb-1)*5)).value = "Moment" 

        # wb.sheets[worksheet_name].range((3+i,1+(nb-1)*5)).value = X[i]
        # wb.sheets[worksheet_name].range((3+i,2+(nb-1)*5)).value = Normal[i] # row, col
        # wb.sheets[worksheet_name].range((3+i,3+(nb-1)*5)).value = Shear[i] 
        # wb.sheets[worksheet_name].range((3+i,4+(nb-1)*5)).value = Moment[i]

    plt.title("Moment force")
    plt.plot(X, Moment, "b", marker="+",label="Moment")
    # plt.plot(X, Shear, "g", marker="*", label="Shear")
    # plt.plot(X, Normal, "r", marker="o", label="Normal")
    plt.plot([0,50, 110, 170, 230, 290 ,340], [0,0,0,0,0,0,0], "g^")
    plt.xlabel('Abscisse')
    plt.ylabel('Effort')
    plt.grid(True)
    plt.legend()
    plt.show()
    # for i_x, i_y in zip(X, Moment):
        # plt.text(i_x, i_y, '({}, {})'.format(i_x, round(i_y,7)))
    # for i_x, i_y in zip(X, Shear):
        # plt.text(i_x, i_y, '({}, {})'.format(i_x, round(i_y,4)))
    # for i_x, i_y in zip(X, Normal):
        # plt.text(i_x, i_y, '({}, {})'.format(i_x, round(i_y,4)))
        
    # print("Mise en place des graphique: " + str(timeit.default_timer()-start))
    # plt.show()
    # """
