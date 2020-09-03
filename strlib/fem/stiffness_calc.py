# Librairy
import timeit
import copy
from typing import Union

# import sympy as sp
import math
import numpy as np

__all__ = ['Point', 'Barre', 'StiffnessMethode', 'Split']


class Point:
    """
        Class to define point element:
        FEM
        Cross section

        This class can be define a "symbolic class"
        it's mean that all calculation will be algerbric

        Class attribute:
        :@param NB_POINT: Nb of point created
        :@type NB_POINT: integer
        :@default NB_POINT: 0 (No elements created)

        Instance attribute:
        :@param name: Name of the point

        :@param x: X coordinate of the point
        :@param y: Y coordinate of the point

        :@param pt_num: point number

        :@param rx: Support reaction in X
        :@param ry: Support reaction in Y
        :@param mt: Support reaction in Moment

        :@param delta_x: Displacement in X
        :@param delta_y: Displacement in Y
        :@param theta: Rotation theta

        :@param rx_cond: Support condition in X
        :@param ry_cond: Support condition in Y
        :@param mt_cond: Support condition in Mz
        :@note: those variable are call if you want
            to define a point as a support

        :@param fx: External force in X
        :@param fy: External force in Y
        :@param mt: External moment

        :@param normal: Internale Normal force
        :@param shear: Internale Shear force
        :@param moment: Internal Bending Moment

        :@type name: int, float, str

        :@type x: int, float
        :@type y: int, float

        :@type pt_num: int

        :@type rx: float
        :@type ry: float
        :@type mt: float

        :@type delta_x: float
        :@type delta_y: float
        :@type theta: float

        :@type rx_cond: boolean
        :@type ry_cond: boolean
        :@type mt_cond: boolean

        :@type fx: float
        :@type fy: float
        :@type mt: float

        :@type normal: float
        :@type shear: float
        :@type moment: float

    """
    NB_POINT = 0

    @classmethod
    def reset(cls):
        """ """
        cls.NB_POINT = 0

    def __init__(self, x: Union[int, float], y: Union[int, float],
                 name: Union[int, float, str] = None, symbolic: bool = False):
        """ Constructor
            :@param x: X coordonate
            :@param y: Y coordonate
            :@param name: Node name
            :@param symbolic: Choose if all calculation will be algerbric
            :@type x: int, double
            :@type y: int, double
            :@type name: int, float, str
            :@type symbolic: boolean
            :@default name: None (No name given)
            :@default symbolic: False (Numerical calculation)
        """
        Point.NB_POINT += 1
        self.__Symbolic_class = symbolic

        # Coordonate
        if symbolic:
            raise NotImplementedError("Not implented yet")
            # self.__define_default_value_symb(name)
        else:
            self.x: Union[int, float] = x
            self.y: Union[int, float] = y
            self.pt_num: int = Point.NB_POINT
            self.__define_default_value(name)

    def __del__(self):
        """ function when an element of the classe if delate """
        Point.NB_POINT -= 1

    def __define_default_value(self, name: str):
        """ Initialize default value
            :@param name: Point Name
            :@type name: string
        """
        # Set value as P_number by default
        if name is None or name == 0 or name is False:
            self.name = "P" + str(Point.NB_POINT)
        else:  # Other the name choosen
            self.name = name

        self.rx: float = 0
        self.ry: float = 0
        self.mt: float = 0

        self.delta_x: float = 0
        self.delta_y: float = 0
        self.theta: float = 0

        # False mean no support
        self.rx_cond: bool = False
        self.ry_cond: bool = False
        self.mt_cond: bool = False

        self.fx: float = 0
        self.fy: float = 0
        self.mz: float = 0

    def define_external_force(self, fx, fy, mz):
        """ Function to define external force

            :@param fx: External force in X
            :@param fy: External force in Y
            :@param mz: External moment in Z
            :@type fx: double
            :@type fy: double
            :@type mz: double
        """
        self.fx = fx
        self.fy = fy
        self.fz = mz

    def define_internal_force(self, fx: Union[int, float],
                              fy: Union[int, float], mz: Union[int, float]):
        """ Function to define external force

            :@param fx: Normal node force
            :@param fy: Shear node force
            :@param mz: Moment node force
            :@type fx: float
            :@type fy: float
            :@type mz: float
        """
        self.normal = fx
        self.shear = fy
        self.moment = mz

    def define_support_reaction(self, rx: Union[int, float],
                                ry: Union[int, float], mt: Union[int, float]):
        """ Function to define support reaction

            :@param rx: X reaction
            :@param ry: Y reaction
            :@param mt: Moment reaction
            :@type rx: float
            :@type ry: float
            :@type mt: float
        """
        self.rx = rx
        self.ry = ry
        self.mt = mt

    def define_displacement(self, dx, dy, theta):
        """ Function to define displacement

            :@param dx: X displacement
            :@param dy: Y displacement
            :@param theta: rotation
            :@type dx: double
            :@type dy: double
            :@type theta: double
        """
        self.delta_x = dx
        self.delta_y = dy
        self.rot = theta

    def define_support_condition(self, rx: bool = False,
                                 ry: bool = False, mt: bool = False):
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
        self.rx_cond = rx
        self.ry_cond = ry
        self.mt_cond = mt

    # Property
    @property
    def hyper_degree(self):
        counter = 0
        if self.rx_cond is True:
            counter += 1
        if self.ry_cond is True:
            counter += 1
        if self.mt_cond is True:
            counter += 1
        return counter


class Barre:
    """
        Class to create barre element
        according to 2 points

        Class attribute:
        :@param __NB_BARRE: Nb of element created
        :@type __NB_BARRE: integer
        :@default __NB_BARRE: 0 (No elements created)

        Instance attribute:
        :@param p_beg:
        :@param p_end:
        :@param beg_type:
        :@param end_type:
        :@param pt_local_beg:
        :@param pt_local_end:

        :@param cross_section:
        :@param material:

        :@param p_beg_name:
        :@param p_end_name:

        :@param pt_num_beg:
        :@param pt_num_end:

        :@param fx_x_beg:
        :@param fx_y_beg:
        :@param fx_m_beg:

        :@param fx_x_end:
        :@param fx_y_end:
        :@param fx_m_end:

        :@param fy_x_beg:
        :@param fy_y_beg:
        :@param fy_m_beg:

        :@param fy_x_end:
        :@param fy_y_end:
        :@param fy_m_end:

        :@param mz_x_beg:
        :@param mz_y_beg:
        :@param mz_m_beg:

        :@param mz_x_end:
        :@param mz_y_end:
        :@param mz_m_end:

        :@param dt_x_beg:
        :@param dt_y_beg:
        :@param dt_m_beg:

        :@param dt_x_end:
        :@param dt_y_end:
        :@param dt_m_end:

        :@param pc_x_beg:
        :@param pc_y_beg:
        :@param pc_m_beg:

        :@param pc_x_end:
        :@param pc_y_end:
        :@param pc_m_end:

        :@param length:
        :@param angle:

        :@param rot_mat:
        :@param k_local_mat:
        :@param k_barre:

        :@param fx:
        :@param fy:
        :@param mz:
        :@param dt_x:
        :@param dt_m:
        :@param pc:

        :@param x_beg:
        :@param y_beg:
        :@param x_end:
        :@param y_end:

    """
    # Attribute
    NB_BARRE = 0

    @classmethod
    def reset(cls):
        """ """
        cls.NB_BARRE = 0

    def __init__(self,  point1: 'Point', point2: 'Point',
                 section: 'Section' = False, material: 'Material' = False,  # noqa: F821, E501
                 beg_type: str = "FIXED", end_type: str = "FIXED",
                 symbolic: bool = False):
        """ Constructor
            :@param point1: 1st node of the barre
            :@param point2: last node of the barre
            :@param section: Barre cross_section
            :@param material: Barre material
            :@param beg_type_: 1st node support condition for calculation
            :@param end_type_: last node support condition for calculation
            :@param symbolic: Choose if all calculation will be algerbric
            :@type point1: Point object
            :@type point2: Point object
            :@type section: TCross_section object or boolean
            :@type material: TMaterial object or boolean
            :@type beg_type_: String
            :@type end_type_: String
            :@type symbolic: boolean
            :@default section: False (mean we take A and I = 1)
            :@default material: False (mean we take E = 1)
            :@default beg_type_: "FIXED"
                (Node condition for the matrix creation)
            :@default end_type_: "FIXED"
                (Node condition for the matrix creation)
            :@default symbolic: False (Numerical calculation)
        """
        Barre.NB_BARRE += 1

        # Point
        self.p_beg: 'Point' = point1
        self.p_end: 'Point' = point2

        self.beg_type: str = beg_type
        self.end_type: str = end_type

        self.pt_local_beg: 'Point' = self.p_beg
        self.pt_local_end: 'Point' = self.p_end

        # Section property
        self.cross_section: 'Section' = section  # noqa: F821
        self.material: 'Material' = material  # noqa: F821

        if symbolic:
            raise NotImplementedError("Not implented yet")
        else:
            self.__default_value()
            self.define_property()

    def __del__(self):
        """ Function when a barre object is delete"""
        Barre.NB_BARRE -= 1

    # Initialisation
    def define_property(self):
        """ Function to define point property """
        self.p_beg_name: 'Point.name' = self.p_beg.name
        self.p_end_name: 'Point.name' = self.p_end.name

        self.p_num_beg: 'Point.pt_num' = self.p_beg.pt_num
        self.p_num_end: 'Point.pt_num' = self.p_end.pt_num

        self.__define_alpha()
        self.__define_length()
        self.__define_rotation_mat()
        self.define_local_mat(self.beg_type, self.end_type)

    def redefine_property(self, point1: 'Point', point2: 'Point',
                 section: 'Section' = False, material: 'Material' = False,  # noqa: F821, E501
                 beg_type: str = "FIXED", end_type: str = "FIXED",
                 symbolic: bool = False):
        """ Function to define point property """
        # Point
        self.p_beg = point1
        self.p_end = point2

        self.beg_type = beg_type
        self.end_type = end_type

        self.pt_local_beg = self.p_beg
        self.pt_local_end = self.p_end

        # Section property
        self.cross_section = section  # noqa: F821
        self.material = material  # noqa: F821
        self.define_property()

    def redefine_force(self):
        """ Function to redifine property after a split """
        fx = self.__fx_force
        fy = self.__fy_force
        mz = self.__mz_force
        kind = self.__kind_force
        angle = self.__angle_force

        self.uniforme_load(fx, fy, mz, kind, angle)

        dt_x = self.__dt_force_x
        dt_m = self.__dt_force_m

        self.temperature(dt_x, dt_m)

        eq = self.__pc_equation
        pc_value = self.__pc_value
        coef = self.__pc_coef
        kind = self.__pc_kind

        self.prestress_load(eq, kind, coef, pc_value)

    def __default_value(self):
        """ Function to define default value """
        self.fx: bool = False
        self.fy: bool = False
        self.mz: bool = False
        self.dt_x: bool = False
        self.dt_m: bool = False
        self.pc: bool = False

        self.__fx_force = 0
        self.__fy_force = 0
        self.__mz_force = 0
        self.__kind_force = "GLOBAL"
        self.__angle_force = 0

        self.__dt_force_x = 0
        self.__dt_force_m = 0

        self.__pc_equation = 0
        self.__pc_value = 0
        self.__pc_coef = 0
        self.__pc_kind = 0

        # Fx
        self.fx_x_beg = 0
        self.fx_y_beg = 0
        self.fx_m_beg = 0

        self.fx_x_end = 0
        self.fx_y_end = 0
        self.fx_m_end = 0

        # Fy
        self.fy_x_beg = 0
        self.fy_y_beg = 0
        self.fy_m_beg = 0

        self.fy_x_end = 0
        self.fy_y_end = 0
        self.fy_m_end = 0

        # Mz
        self.mz_x_beg = 0
        self.mz_y_beg = 0
        self.mz_m_beg = 0

        self.mz_x_end = 0
        self.mz_y_end = 0
        self.mz_m_end = 0

        # dt
        self.dt_x_beg = 0
        self.dt_y_beg = 0
        self.dt_m_beg = 0

        self.dt_x_end = 0
        self.dt_y_end = 0
        self.dt_m_end = 0

        # PC
        self.pc_x_beg = 0
        self.pc_y_beg = 0
        self.pc_m_beg = 0

        self.pc_x_end = 0
        self.pc_y_end = 0
        self.pc_m_end = 0

    def __define_length(self):
        """ Function to define the length of the barre """
        x_beg = self.p_beg.x
        y_beg = self.p_beg.y

        x_end = self.p_end.x
        y_end = self.p_end.y

        self.length = math.sqrt((x_end - x_beg)**2 + (y_end - y_beg)**2)

    def __define_alpha(self):
        """ Function to define the angle of the barre
            compare to a default axe |_ -> _ (x) ; | (y)
        """
        x_beg = self.p_beg.x
        y_beg = self.p_beg.y

        x_end = self.p_end.x
        y_end = self.p_end.y

        if (x_end - x_beg) != 0:
            atan = math.atan((y_end - y_beg)/(x_end - x_beg))
            angle = math.degrees(atan)
        else:
            sign = math.copysign(1, (y_end - y_beg))
            angle = sign * 90

        self.angle: float = angle

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
        angle_rad = math.radians(self.angle)
        cos, sin = math.cos(angle_rad), math.sin(angle_rad)

        self.rot_mat: 'numpy float' = np.array([[cos, sin, 0, 0, 0, 0],  # noqa: F722, E501
                                               [-sin, cos, 0, 0, 0, 0],
                                               [0, 0, 1, 0, 0, 0],
                                               [0, 0, 0, cos, sin, 0],
                                               [0, 0, 0, -sin, cos, 0],
                                               [0, 0, 0, 0, 0, 1]],
                                               dtype=float)

    def define_local_mat(self, beg_type: str = "FIXED",
                         end_type: str = "FIXED"):
        """ Function to define local stiffness matrix to all element
            in local axes
            :@param beg_type: 1st node of the barre
            :@param end_type: 1st node of the barre
            :@type beg_type: String
            :@type end_type: String
            :@default beg_type: FIXED (for frame element)
            :@default end_type: FIXED (for frame element)
            :@other beg_type: PINED (Truss element); LINTEL (Lintel element)
            :@other end_type: PINED (Truss element); LINTEL (Lintel element)
        """
        # Coefficient
        L = self.length
        if self.material is False and self.cross_section is False:
            eal: float = 1 * 1 / L
            ei: int = 1 * 1
        else:
            eal: float = self.material.E * self.cross_section.area / L
            ei: float = self.material.E * self.cross_section.inertia_y

        # Matrix definition
        if beg_type == "FIXED" and end_type == "FIXED":
            self.k_local: 'numpy float' = np.array([  # noqa: F722
                                                   [eal, 0, 0, -eal, 0, 0],
                                                   [0, 12 * ei / (L**3), 6 * ei / (L**2), 0, -12 * ei / (L**3), 6 * ei / (L**2)],  # noqa: E501
                                                   [0, 6 * ei / (L**2), 4 * ei / L, 0, -6 * ei / (L**2), 2 * ei / L],  # noqa: E501
                                                   [-eal, 0, 0, eal, 0, 0],
                                                   [0, -12 * ei / (L**3), -6 * ei / (L**2), 0, 12 * ei / (L**3), -6 * ei / (L**2)],  # noqa: E501
                                                   [0, 6 * ei / (L**2), 2 * ei / L, 0, -6 * ei / (L**2), 4 * ei / L]], dtype=float)  # noqa: E501
        elif beg_type == "PINED" and end_type == "FIXED":  # Need a vérification # noqa: E501
            self.k_local: 'numpy float' = np.array([  # noqa: F722
                                                   [eal, 0, 0, -eal, 0, 0],
                                                   [0, 3 * ei / (L**3), 0, 0, -3 * ei / (L**3), 3 * ei / (L**2)],  # noqa: E501
                                                   [0, 0, 0, 0, 0, 0],
                                                   [-eal, 0, 0, eal, 0, 0],
                                                   [0, -3 * ei / (L**3), 0, 0, 3 * ei / (L**3), -3 * ei / (L**2)],  # noqa: E501
                                                   [0, 3 * ei / (L**2), 0, 0, -3 * ei / (L**2), 3 * ei / L]], dtype=float)  # noqa: E501

        elif beg_type == "FIXED" and end_type == "PINED":  # Need a vérification # noqa: E501
            self.k_local: 'numpy float' = np.array([  # noqa: F722
                                                   [eal, 0, 0, -eal, 0, 0],
                                                   [0, 3 * ei / (L**3), 3 * ei / (L**2), 0, -3 * ei / (L**3), 0],  # noqa: E501
                                                   [0, 3 * ei / (L**2), 3 * ei / L, 0, -3 * ei / (L**2), 0],  # noqa: E501
                                                   [-eal, 0, 0, eal, 0, 0],
                                                   [0, -3 * ei / (L**3), -3 * ei / (L**2), 0, 3 * ei / (L**3), 0],  # noqa: E501
                                                   [0, 0, 0, 0, 0, 0]], dtype=float)  # noqa: E501
        elif beg_type == "PINED" and end_type == "PINED":
            self.k_local: 'numpy float' = np.arra([  # noqa: F722
                                                  [eal, 0, 0, -eal, 0, 0],
                                                  [0, 0, 0, 0, 0, 0],
                                                  [0, 0, 0, 0, 0, 0],
                                                  [-eal, 0, 0, eal, 0, 0],
                                                  [0, 0, 0, 0, 0, 0],
                                                  [0, 0, 0, 0, 0, 0]], dtype=float)   # noqa: E501
        elif beg_type == "LINTEL" and end_type == "LINTEL":  # Need a vérification - HB IGH # noqa: E501
            """
            self.k_local: 'numpy float' = np.arra([
                [0, 0, 0, 0, 0, 0],
                [0, 3, 3 * (b1 + a),0 ,-3, 3 * (b2 + a)],
                [0, 3 * (b1 + a), 3 * b1**2 + 6 * a * b1 + 4 * a**2, 0, -3 * (b1 + a), 3 * (b1 + a) * (b2 + a) - a**2], # noqa: E501
                [0, 0, 0, 0, 0, 0],
                [0, -3, -3 * (b1 + a), 0, 3, 3 * (b2 + a)],
                [0, 3 * (b2 + a), 3 * (b1 + a) * (b2 + a) - a**2, 0, 3 * (b2 + a), 3 * b2**2 + 6 * a * b2 + 4 * a**2]], dtype=float) # noqa: E501
            """
            raise NotImplementedError

        self.__define_k_barre_mat()

    def __define_k_barre_mat(self):
        """ Function to define local stiffness matrix to all element
            in global axes
        """
        rot_t_ = np.transpose(self.rot_mat)
        self.k_barre: 'numpy float' = np.matmul(   # noqa: F722
                    np.matmul(rot_t_, self.k_local),
                    self.rot_mat)

    def uniforme_load(self, fx: bool, fy: bool, mz: bool, kind: str = "GLOBAL", angle: float = 0):  # noqa: E501
        """ Function to define uniforme load on the barre

            fx, fy, mz are global value

            :@param fx: uniforme fx
            :@param fy: uniforme fy
            :@param mz: uniforme mz
            :@type fx: double
            :@type fy: double
            :@type mz: double
        """
        L = self.length
        # angle_barre_rad = math.radians(self.angle)
        # cos_barre = math.cos(angle_barre_rad)
        # sin_barre = math.sin(angle_barre_rad)

        self.fx: bool = True if fx != 0 else False
        self.fy: bool = True if fy != 0 else False
        self.mz: bool = True if mz != 0 else False

        self.__fx_force = fx
        self.__fy_force = fy
        self.__mz_force = mz
        self.__kind_force = kind
        self.__angle_force = angle

        # Fx

        # Fy
        if kind == "GLOBAL":
            # angle_force_rad_ = math.radians(angle)
            # cos_force_ = math.cos(angle_force_rad_)
            # sin_force_ = math.sin(angle_force_rad_)

            self.fy_x_beg = 0  # fy * l_/2 * sin_barre_ * sin_force_
            self.fy_y_beg = fy * L / 2  # * cos_barre_ * cos_force_
            self.fy_m_beg = fy * L**2 / 12  # * cos_barre_ * cos_force_

            self.fy_x_end = 0  # -fy * l_/2  * sin_barre_ * sin_force_
            self.fy_y_end = fy * L / 2  # * cos_barre_ * cos_force_
            self.fy_m_end = -fy * L**2 / 12  # * cos_barre_ * cos_force_
        else:
            self.fy_x_beg = fy * L / 2
            self.fy_y_beg = fy * L / 2
            self.fy_m_beg = fy * L**2 / 12

            self.fy_x_end = 0
            self.fy_y_end = fy * L / 2
            self.fy_m_end = -fy * L**2 / 12

    def temperature(self, dT_x: float, dT_m: float):
        """
            Function to define uniforme load on the barre

            :@param dT_x: thermal load in X axis
            :@param dT_m: thermal load in Z axis
            :@type dT_x: float
            :@type dT_m: float
        """

        self.dt_x: bool = True if dT_x != 0 else False
        self.dt_m: bool = True if dT_m != 0 else False

        self.__dt_force_x = dT_x
        self.__dt_force_m = dT_m

        if self.material is False and self.cross_section is False:
            E = 1
            Iy = 1
            alpha = 1
            h = 1
            A = 1
        else:
            E = self.material.E
            Iy = self.cross_section.inertia_y
            A = self.cross_section.area
            alpha = self.material.alpha
            h = self.cross_section.h

        self.dt_x_beg = E * A * alpha * dT_x / self.length
        self.dt_y_beg = 0
        self.dt_m_beg = E * Iy * alpha * dT_m / h

        self.dt_x_end = -E * A * alpha * dT_x / self.length
        self.dt_y_end = 0
        self.dt_m_end = -E * Iy * alpha * dT_m / h

    def prestress_load(self, equation, kind="RIVE", coef=[], prestress_value=1):  # A FAIRE # noqa: E501
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
            :@default prestress_value: 1 (to considere in function of th prestress) # noqa: E501
        """

        self.pc = True if prestress_value != 0 else False

        self.__pc_equation = equation
        self.__pc_value = prestress_value
        self.__pc_coef = coef
        self.__pc_kind = kind

        x_beg_ = self.pt_local_beg.x
        y_beg_ = self.pt_local_beg.y

        x_end_ = self.pt_local_end.x
        y_end_ = self.pt_local_end.y

        Length_ = math.sqrt((x_end_-x_beg_)**2 + (y_end_-y_beg_)**2)

        if type(equation) == float or type(equation) == int:
            self.pc_x_beg = -prestress_value
            self.pc__y_beg = 0
            self.pc__m_beg = prestress_value * equation

            self.pc__x_end = -prestress_value
            self.pc__y_end = 0
            self.pc__m_end = -prestress_value * equation

        else:
            if kind == "RIVE":
                L_alpha_L = coef[0]  # (1-alpha)*L
                # alpha_L = coef[1]

                X_beg = self.p_beg.x
                X_end = self.p_end.x

                if X_end > Length_:
                    X_beg -= self.pt_local_beg.x
                    X_end -= self.pt_local_beg.x

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

                eq_beg = a * X_beg**2 + b * X_beg + c
                eq_end = a * X_end**2 + b * X_end + c

                # Beg
                f_a_beg = eq_beg
                f_p_a_beg = 2 * a * eq_beg + b

                y_0_beg = f_a_beg + f_p_a_beg * (0 - eq_beg)
                y_1_beg = f_a_beg + f_p_a_beg * (1 - eq_beg)

                a_angle_beg = y_0_beg - y_1_beg
                b_angle_beg = 1

                angle_beg = math.atan(-a_angle_beg / b_angle_beg)

                # End
                f_a_end = eq_end
                f_p_a_end = 2 * a * eq_end + b

                y_0_end = f_a_end + f_p_a_end * (0 - eq_end)
                y_1_end = f_a_end + f_p_a_end * (1 - eq_end)

                a_angle_end = y_0_end - y_1_end
                b_angle_end = 1

                angle_end = math.atan(-a_angle_end / b_angle_end)

            elif kind == "INTER":
                beta_L = coef[0]  # (1-alpha)*L
                L_beta_gamma_L = coef[1]  # (1-beta-gamma)*L
                # gamma_L = coef[2]

                X_beg = self.p_beg.x
                X_end = self.p_end.x

                X_beg -= self.pt_local_beg.x
                X_end -= self.pt_local_end.x

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

                eq_beg = a * X_beg**2 + b * X_beg + c
                eq_end = a * X_end**2 + b * X_end + c

                # Beg
                f_a_beg = eq_beg
                f_p_a_beg = 2*a*eq_beg + b

                y_0_beg = f_a_beg + f_p_a_beg * (0 - eq_beg)
                y_1_beg = f_a_beg + f_p_a_beg * (1 - eq_beg)

                a_angle_beg = y_0_beg - y_1_beg
                b_angle_beg = 1

                angle_beg = math.atan(-a_angle_beg / b_angle_beg)

                # End
                f_a_end = eq_end
                f_p_a_end = 2 * a * eq_end + b

                y_0_end = f_a_end + f_p_a_end * (0 - eq_end)
                y_1_end = f_a_end + f_p_a_end * (1 - eq_end)

                a_angle_end = y_0_end - y_1_end
                b_angle_end = 1

                angle_end = math.atan(-a_angle_end / b_angle_end)

            self.pc_x_beg = -prestress_value
            self.pc_y_beg = 0
            self.pc_m_beg = prestress_value * eq_beg * math.cos(angle_beg)

            self.pc_x_end = -prestress_value
            self.pc_y_end = 0
            self.pc_m_end = -prestress_value * eq_end * math.cos(angle_end)

    # Special methode

    # def __repr__(self):
        # """ used when you print(Barre object) """
        # if self.NB_BARRE == 1:
            # return "It exist {} element ".format(self.__NB_BARRE)
        # else:
            # return "It exist {} element".format(self.__NB_BARRE)


class StiffnessMethode:
    """
        Class to do calculation

        This class can be define a "symbolic class"
        it's mean that all calculation will be algerbric

        Class variable:
        :@param __INTERVAL_POINT:
        :@param SUM_EQ:
        :@type __INTERVAL_POINT: integer
        :@type SUM_EQ: integer
        :@default __INTERVAL_POINT: 50 (Number of point between two node to make graphic) # noqa: E501
        :@default SUM_EQ: 3 (Number of equation by node)

        Instance variable:
        :@param support_tab:
        :@param d_tab:
        :@param force_tab:
        :@param connect_tab:
        :@param k_global:
        :@param unds_tab:

        :@type support_tab: numpy int
        :@type d_tab: numpy float ?
        :@type force_tab: numpy float
        :@type connect_tab: numpy int
        :@type k_global: numpy float
        :@type unds_tab: numpy float
    """
    # Attribute
    __INTERVAL_POINT = 50
    SUM_EQ = 3

    def __init__(self, point_array: 'Point', barre_array: 'Barre',
        symbolic: bool = False):
        """ Constructor
            :@param barre_array: tuple of all barre
            :@param point_array: tuple of all point
            :@param symbolic: Choose if all calculation will be algerbric
            :@type barre_array: tuple
            :@type point_array: tuple
            :@type symbolic: bool
        """
        self.__point_tab: 'Point' = point_array
        self.__barre_tab: 'Barre' = barre_array
        
        # Lintel variable

        # self.__a = None
        # self.__b = None

        # Calculation
        self.__routine_calculation()

    def __routine_calculation(self):
        """ Function to make and remake all calculaion """

        # Define element
        self.__define_Support_tab()
        self.__define_D_tab()
        self.__define_Force_tab()

        # Define matrix
        start = timeit.default_timer()
        self.__define_connection_table()
        print("     Definition of connection table: " + str(timeit.default_timer()-start))  # noqa: E501
        start = timeit.default_timer()
        self.__define_global_stiffness_mat()
        print("     Definition of the global stiffness matrix: " + str(timeit.default_timer()-start))  # noqa: E501
        # Calculation

        self.__mat_modif()
        self.__calc_D_Rint()
        self.__fill_point()
        self.__interne_force()
        self.__write_interal_force()

    def __define_Support_tab(self):
        """ Function to fill support matrix
            support_tab  = [Rax, Ray, M]
            1 mean reaction existe
            0 mean reaction doesn't existe
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.support_tab: 'numpy int' = np.zeros(point)
        counter = 0

        for i in self.__point_tab:
            self.support_tab[counter] = 1 if i.rx_cond is True else 0
            self.support_tab[counter+1] = 1 if i.ry_cond is True else 0
            self.support_tab[counter+2] = 1 if i.mt_cond is True else 0
            counter += 3

    def __define_D_tab(self):
        """ Function to fill displacement tab
            d_tab  = [dx, dy, theta]
            1 mean displacement existe
            0 mean displacement doesn't existe
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.d_tab = np.zeros(point)

        self.__sum_int = 0  # sum of unknown reaction

        for i in range(0, point):
            if self.support_tab[i] == 1:
                self.d_tab[i] = 0
                self.__sum_int += 1
            else:
                self.d_tab[i] = 1

    def __define_Force_tab(self):
        """ Function to fill force tab
            __Force_tab  = [Fx, Fy, Mt]
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.force_tab: 'numpy float' = np.zeros(point)  # (1,point)
        counter = 0
        # barre_done_ = []

        for i in self.__point_tab:
            self.force_tab[counter] = i.fx
            self.force_tab[counter+1] = i.fy
            self.force_tab[counter+2] = i.mz

            for ii in self.__barre_tab:
                if (ii.fx or ii.fy or ii.mz or ii.dt_x or ii.dt_m or ii.pc):  # noqa: E501
                    if i.name == ii.p_beg_name:
                        self.force_tab[counter] += ii.fx_x_beg \
                            + ii.fy_x_beg + ii.mz_x_beg \
                            + ii.dt_x_beg + ii.pc_x_beg
                        self.force_tab[counter+1] += ii.fx_y_beg \
                            + ii.fy_y_beg + ii.mz_y_beg \
                            + ii.dt_y_beg + ii.pc_y_beg
                        self.force_tab[counter+2] += ii.fx_m_beg \
                            + ii.fy_m_beg + ii.mz_m_beg \
                            + ii.dt_m_beg + ii.pc_m_beg

                    elif i.name == ii.p_end_name:
                        self.force_tab[counter] += ii.fx_x_end \
                            + ii.fy_x_end + ii.mz_x_end \
                            + ii.dt_x_end + ii.pc_x_end
                        self.force_tab[counter+1] += ii.fx_y_end \
                            + ii.fy_y_end + ii.mz_y_end \
                            + ii.dt_y_end + ii.pc_y_end
                        self.force_tab[counter+2] += ii.fx_m_end \
                            + ii.fy_m_end + ii.mz_m_end \
                            + ii.dt_m_end + ii.pc_m_end
            counter += 3

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
        col = len(self.__point_tab)
        row = Barre.NB_BARRE

        row_b = 0
        self.connect_tab: 'numpy int' = np.zeros((row, col))

        for barre in self.__barre_tab:
            col_b = 0
            for pt in self.__point_tab:
                if barre.p_beg_name == pt.name or \
                    barre.p_end_name == pt.name:
                    self.connect_tab[row_b, col_b] = 1
                else:
                    self.connect_tab[row_b, col_b] = 0
                col_b += 1
            row_b += 1

    def __define_global_stiffness_mat(self):
        """ Function to mix the global stifness matrix """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.k_global: 'numpy float' = np.zeros((point, point), dtype=float)
        pass_ = np.zeros(Barre.NB_BARRE)

        for i in range(0, Point.NB_POINT * 3, 3):
            for ii in range(0, Point.NB_POINT * 3, 3):
                for iii in range(0, Barre.NB_BARRE):
                    my_tab = self.__barre_tab[iii].k_barre

                    if self.connect_tab[iii, int(i / 3)] != 0 and \
                       self.connect_tab[iii, int(ii / 3)] != 0:
                        if i == 0 and ii == 0:  # k11
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.k_global[j, jj] += self.connect_tab[iii, int(ii / 3)] * \
                                        self.connect_tab[iii, int(i / 3)] * my_tab[j - i, jj - ii]
                            pass_[iii] = 1
                        elif i == ii:  # k11 + k22
                            if pass_[iii] == 1:
                                for j in range(i, i + 3):
                                    for jj in range(ii, ii + 3):
                                        self.k_global[j, jj] += self.connect_tab[iii, int(ii / 3)] * \
                                            self.connect_tab[iii, int(i / 3)] * \
                                            my_tab[j - i + 3, jj - ii + 3]
                            else:
                                for j in range(i, i + 3):
                                    for jj in range(ii, ii + 3):
                                        self.k_global[j, jj] += self.connect_tab[iii, int(i / 3)] * \
                                            self.connect_tab[iii, int(i / 3)] * \
                                            my_tab[j - i, jj - ii]
                                pass_[iii] = 1
                        elif i + 3 == ii:  # k12
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.k_global[j, jj] += + self.connect_tab[iii, int(ii / 3)] * \
                                        self.connect_tab[iii, int(i / 3)] * \
                                        my_tab[j - i, jj - ii + 3]
                        elif i == ii + 3:  # k21
                            for j in range(i, i + 3):
                                for jj in range(ii, ii + 3):
                                    self.k_global[j, jj] += self.connect_tab[iii, int(ii / 3)] * \
                                        self.connect_tab[iii, int(i / 3)] * \
                                        my_tab[j - i + 3, jj - ii]

    def __mat_modif(self):
        """ Multiply k_global by D_tab
            Removing zero form D_tab
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        kxd = np.zeros((point, point), dtype=float)
        k_d_wz = np.zeros((point, point), dtype=float)
        b = 0
        pass_ = False

        for i in range(0, point):  # Row
            a = 0
            for ii in range(0, point):  # Col
                kxd[ii, i] = self.k_global[i, ii] * self.d_tab[i]
                if self.d_tab[i] != 0:
                    k_d_wz[a, b] = kxd[ii, i]
                    a += 1
                    pass_ = True
            if pass_:
                b += 1
                pass_ = False

        self.__k_d_wz_r = k_d_wz

        a = point - 1

        for i in range(point-1, -1, -1):
            if self.support_tab[i] != 0:
                for ii in range(point-1, -1, -1):
                    if ii == i:
                        self.__k_d_wz_r[ii, a] = -1
                a -= 1

    def __calc_D_Rint(self):
        """ Calculate the matrix of displacement
            and support reaction

            Support reaction will alway be at the end_type_
            [dx, dy, rx, ry]
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.unds_tab: 'numpy float' = np.zeros(point)

        start = timeit.default_timer()
        mat_inverse = np.linalg.inv(self.__k_d_wz_r)  # Matrix inversion
        print("         Inversion de la matrice de rigidité: " + str(timeit.default_timer()-start))
        self.unds_tab = np.matmul(mat_inverse, self.force_tab)

    def __fill_point(self):
        """ fill reaction in point
            fill displacement in point
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        self.__delta_theta_str = np.zeros(point)
        a = 0
        b = 0

        for i in range(0, point):
            if self.support_tab[i] == 1:
                if i % 3 == 0:
                    self.__point_tab[int(i/3)].rx = self.unds_tab[point - self.__sum_int + a]
                elif i % 3 == 1:
                    self.__point_tab[int((i-1)/3)].ry = self.unds_tab[point - self.__sum_int + a]
                elif i % 3 == 2:
                    self.__point_tab[int((i-2)/3)].mt = self.unds_tab[point - self.__sum_int + a]
                a += 1

            if self.d_tab[i] == 1:
                if i % 3 == 0:
                    self.__point_tab[int(i/3)].delta_x = self.unds_tab[b]
                elif i % 3 == 1:
                    self.__point_tab[int((i-1)/3)].delta_y = self.unds_tab[b]
                elif i % 3 == 2:
                    self.__point_tab[int((i-1)/3)].theta = self.unds_tab[b]
                self.__delta_theta_str[i] = self.unds_tab[b]
                b += 1
            else:
                if i % 3 == 0:
                    self.__point_tab[int(i/3)].delta_x = 0
                elif i % 3 == 1:
                    self.__point_tab[int((i-1)/3)].delta_y = 0
                elif i % 3 == 2:
                    self.__point_tab[int((i-2)/3)].theta = 0
                self.__delta_theta_str[i] = 0

    def __interne_force(self):
        """ calculate internal force
            fill in odered fonction of node
        """
        point = Point.NB_POINT * self.SUM_EQ  # Number of point
        tmp_delta = np.zeros(self.SUM_EQ * 2)

        self.__NSM_effort: 'numpy float' = np.zeros(point)
        
        for i in self.__barre_tab:
            for ii in range(0, 3):
                tmp_delta[ii] = self.__delta_theta_str[i.p_num_beg * 3 + ii - 3]
                tmp_delta[ii+3] = self.__delta_theta_str[i.p_num_end * 3 + ii - 3]

            tmp = np.matmul(i.k_local, i.rot_mat)
            NSM_tmp = np.matmul(tmp, tmp_delta)

            for ii in range(0, 3):
                if ii == 0:  # Fx
                    add_beg = i.fx_x_beg + i.fy_x_beg + i.mz_x_beg + i.dt_x_beg + i.pc_x_beg
                    add_end = i.fx_x_end + i.fy_x_end + i.mz_x_end + i.dt_x_end + i.pc_x_end
                elif ii == 1:  # Fy
                    add_beg = i.fx_y_beg + i.fy_y_beg + i.mz_y_beg + i.dt_y_beg + i.pc_y_beg
                    add_end = i.fx_y_end + i.fy_y_end + i.mz_y_end + i.dt_y_end + i.pc_y_end
                elif ii == 2:  # Mz
                    add_beg = i.fx_m_beg + i.fy_m_beg + i.mz_m_beg + i.dt_m_beg + i.pc_m_beg
                    add_end = i.fx_m_end + i.fy_m_end + i.mz_m_end + i.dt_m_end + i.pc_m_end
                self.__NSM_effort[i.p_num_beg*3+ii-3] = NSM_tmp[ii] - add_beg
                self.__NSM_effort[i.p_num_end*3+ii-3] = -NSM_tmp[ii+3] + add_end


    def __write_interal_force(self):
        """ fill force in point """
        ii = 0
        for i in self.__point_tab:
            i.define_internal_force(self.__NSM_effort[ii], self.__NSM_effort[ii+1],
                                    self.__NSM_effort[ii+2])
            ii += 3

    @classmethod
    def test_iso(cls, point_array):
        """
            Class methode
            Function to know the hyperstaticity of the structure
            @parma point_array: List of all point
            @type point_array: tuple

            @param return: Hypostatic; Isostatique; Hyperstatic
            @type return: String
        """
        counter = -3
        for pt in point_array:
            counter += pt.hyper_degree
        if counter < 0:
            return "Hypostatic"
        elif counter == 0:
            return "Isostatique"
        else:
            return "Hyperstatic"


class Split:
    """
        this class is for splitting the barre
    """

    def __init__(self, p_beg, p_end, Barre, step, point_all, barre_all):
        """
           Constructor

            :@type p_beg:
        """
        self.__Step = step
        self.__Point = []
        self.__Barre = []

        self.__Point_all = point_all
        self.__Barre_all = barre_all

        self.__Barre_lmt = Barre

        self.__Pt_beg = p_beg
        self.__Pt_end = p_end

        self.__Pt_beg_Name = p_beg.name
        self.__Pt_end_Name = p_end.name

        self.__Pt_X_beg = p_beg.x
        self.__Pt_X_end = p_end.x

        self.__Pt_Y_beg = p_beg.y
        self.__Pt_Y_end = p_end.y

        self.__devide_point()
        self.__devide_barre()
        self.__rename_elmt()

    def __devide_point(self):
        """
            function to create all sub point between two point
            ! Work only for y = 0
        """

        if self.__Pt_Y_beg == 0 and self.__Pt_Y_end == 0:

            Length = abs(self.__Pt_X_beg - self.__Pt_X_end)
            step_tab = np.arange(0.0, (Length + Length / self.__Step), Length / self.__Step)
            step_name = Length * Length / self.__Step
            Name = self.__Pt_beg_Name + self.__Pt_end_Name

            value_name = step_name

            for i in step_tab:
                if i != 0 and round(i, 15) < Length:
                    X = self.__Pt_X_beg
                    new_name = Name + " " + str(value_name)
                    point = Point(X + i, 0, new_name)
                    self.__Point.append(point)
                    value_name += step_name
                elif i == 0:
                    self.__Point.append(self.__Pt_beg)
                elif round(i, 15) == Length:
                    self.__Point.append(self.__Pt_end)
                    break

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
                self.__Barre[counter_].p_beg = self.__Point[i]
                self.__Barre[counter_].p_end = self.__Point[i+1]
                self.__Barre[counter_].pt_local_beg = self.__Barre_lmt.p_beg
                self.__Barre[counter_].pt_local_end = self.__Barre_lmt.p_end
                self.__Barre[counter_].define_property()
                self.__Barre[counter_].redefine_force()

                counter_ += 1
            Barre.NB_BARRE += counter_ - 1

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
            for i in range(0, Length_):
                if self.__Barre_all[i] == self.__Barre_lmt:
                    for ii in self.__Barre:
                        if counter_ == 0:
                            if i == 0:
                                self.__Point[0].pt_num = 1
                                self.__Point[1].pt_num = 2

                                Point_tmp.append(self.__Point[0])
                                Point_tmp.append(self.__Point[1])

                                ii.p_num_beg = 1
                                ii.p_num_end = 2
                                Barre_tmp.append(ii)
                            else:
                                P_beg_num = self.__Barre_all[i].p_num_beg
                                P_end_num = P_beg_num + 1
                                self.__Point[counter_+1].pt_num = P_end_num

                                Point_tmp.append(self.__Point[counter_+1])

                                ii.p_num_end = P_end_num
                                Barre_tmp.append(ii)
                        else:
                            P_beg_num = Barre_tmp[i+counter_-1].p_num_end
                            P_end_num = P_beg_num + 1

                            self.__Point[counter_+2-1].pt_num = P_end_num

                            Point_tmp.append(self.__Point[counter_+2-1])

                            ii.p_num_beg = P_beg_num
                            ii.p_num_end = P_end_num
                            Barre_tmp.append(ii)

                        counter_ += 1
                    pass_ = True

                elif pass_ is True:
                    P_beg_num = Barre_tmp[i+counter_-1-1].p_num_end
                    P_end_num = P_beg_num + 1

                    self.__Barre_all[i].p_num_beg = P_beg_num
                    self.__Barre_all[i].p_num_end = P_end_num

                    self.__Barre_all[i].p_end.pt_num = P_end_num

                    Point_tmp.append(self.__Barre_all[i].p_end)

                    Barre_tmp.append(self.__Barre_all[i])

                elif pass_ is False:
                    if i == 0:
                        Point_tmp.append(self.__Barre_all[i].p_beg)
                        Point_tmp.append(self.__Barre_all[i].p_end)
                        Barre_tmp.append(self.__Barre_all[i])
                    else:
                        Point_tmp.append(self.__Barre_all[i].p_end)
                        Barre_tmp.append(self.__Barre_all[i])
        else:
            for ii in self.__Barre:
                if counter_ == 0:
                    self.__Point[0].pt_num = 1
                    self.__Point[1].pt_num = 2

                    Point_tmp.append(self.__Point[0])
                    Point_tmp.append(self.__Point[1])

                    ii.p_num_beg = 1
                    ii.p_num_end = 2
                    Barre_tmp.append(ii)
                else:
                    P_beg_num = Barre_tmp[counter_-1].p_num_end
                    P_end_num = P_beg_num + 1

                    self.__Point[counter_+2-1].pt_num = P_end_num

                    Point_tmp.append(self.__Point[counter_+2-1])

                    ii.p_num_beg = P_beg_num
                    ii.p_num_end = P_end_num
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

    P1 = Point(0,0)
    P2 = Point(1,0)
    P3 = Point(2,0)

    P1.define_support_condition(True, True, False)
    P3.define_support_condition(True, True, False)

    P2.define_external_force(0,-10,0)

    B1 = Barre(P1, P2)
    B2 = Barre(P2, P3)

    point = (P1, P2, P3)
    barre = (B1, B2)

    nb_devid = 10

    my_eltm = Split(P1, P2, B1, nb_devid, point, barre)
    
    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = Split(P2, P3, B2, nb_devid, point, barre)
    
    point = my_eltm.Point
    barre = my_eltm.Barre
   
    result = StiffnessMethode(point, barre)

    import matplotlib.pyplot as plt

    X = []
    Moment = []
    for i in point:
        X.append(i.x)
        Moment.append(i.moment)

    plt.title("Moment force")
    plt.plot(X, Moment, "b", marker="+", label="Moment")
    plt.show()

"""
   # start = timeit.default_timer()

   # my_sec = sec.TCustom()
   # my_sec.Area = 11.333 # m2
   # my_sec.Inertia_y = 25.5375 # m4
   # my_sec.H = 4.2 # m

   # my_mat = mat.TMaterial()

   # my_mat.E = 35000 # MPa
    #my_mat.Alpha = 10 * 10**(-6)

    P1 = Point(0,0)
    P2 = Point(50,0)
    P3 = Point(110,0)
    P4 = Point(170,0)
    P5 = Point(230,0)
    P6 = Point(290,0)
    P7 = Point(340,0)

    P1.define_support_condition(True,True,False)
    P2.define_support_condition(True,True,False)
    P3.define_support_condition(True,True,False)
    P4.define_support_condition(True,True,False)
    P5.define_support_condition(True,True,False)
    P6.define_support_condition(True,True,False)
    P7.define_support_condition(True,True,False)

    B1 = Barre(P1, P2)  #, my_sec, my_mat)
    B2 = Barre(P2, P3)#, my_sec, my_mat)
    B3 = Barre(P3, P4)#, my_sec, my_mat)
    B4 = Barre(P4, P5)#, my_sec, my_mat)
    B5 = Barre(P5, P6)#, my_sec, my_mat)
    B6 = Barre(P6, P7)#, my_sec, my_mat)

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

    my_eltm = Split(P1, P2, B1, nb_devid, point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    print("Division d'un élément: " + str(timeit.default_timer()-start))
    print("\n")

    my_eltm = Split(P2, P3, B2, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = Split(P3, P4, B3, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = Split(P4, P5, B4, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = Split(P5, P6, B5, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    my_eltm = Split(P6, P7, B6, nb_devid , point, barre)

    point = my_eltm.Point
    barre = my_eltm.Barre

    # os.system("pause")

    print("Division de tous les éléments: " + str(timeit.default_timer()-start_2))

    print("\n")
    print("Lancement des calculs:")
    start = timeit.default_timer()
    print(" Nb de point: " + str(len(point)))
    print(" Nb de barre: " + str(len(barre)))
    result = StiffnessMethode(barre, point)

    print("Fin du calcul: " + str(timeit.default_timer()-start))

    # start = timeit.default_timer()

    import matplotlib.pyplot as plt
    # import xlwings as xw
    X = []
    Moment = []
    for i in point:
        X.append(i.X)
        Moment.append(i.Moment)

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
 #         wb.sheets[worksheet_name].range((2+i,3)).value = Shear[i]
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

    plt.show()
"""
