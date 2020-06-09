from TFem import TPoint, TBarre, TStiffness_methode

import numpy as np
import matplotlib.pyplot as plt

import sys, os
import timeit


def main():

    start = timeit.default_timer()

    point = []
    barre = []
    
    ap_1 = 50
    ap_2 = 60
    ap_3 = 60
    ap_4 = 60
    ap_5 = 60
    ap_6 = 50
    Length = ap_1+ap_2+ap_3+ap_4+ap_5+ap_6 # 340 m
    step = 10 # m
    
    step_tab = np.arange(0.0, (Length+1), step)
    
    counter_ = 0
    
    for i in step_tab:
        
        point_ = TPoint(0+i,0)
        point.append(point_)
       
        if i == 20:
            point[counter_].define_external_force(0,-1,0)
        
        if i == 0 or i == 50 or i == 110 or i == 170 \
            or i == 230 or i == 290 \
            or  i == Length:
            point[counter_].define_support_condition(True,True,False)
        
        counter_ += 1

    for i in step_tab:
        
        ii = int(i/step)-step
        barre_ = TBarre(point[ii], point[ii+1])
        barre.append(barre_)
   
    print("Lancement des calculs")
    # print(len(point))
    # print(len(barre))
    rslt = TStiffness_methode(barre, point)

    print("Calculs fini")
    # for i in barre:
        # print(i.P_beg_name + " AND " + i.P_end_name)
    X = []
    Moment = []
    for i in point:
        # print(i.Name)
        X.append(i.X)
        Moment.append(i.Moment)
        # print("Support")
        # print(i.Rx)
        # print(i.Ry)
        # print(i.Mt)
        # print("Internal")
        # print(i.Normal)
        # print(i.Shear)
        # print(i.Moment)
        # print("Displacement")
        # print(i.Delta_x)
        # print(i.Delta_y)
        # print(i.Theta)
        # print("")

    stop = timeit.default_timer()
    
    print('Time: ', stop - start, ' sec')  

    plt.title("Moment force en X = 25")
    plt.plot(X, Moment, "bs")
    plt.plot([0,50,110,170,230,290,340], [0,0,0,0,0,0,0], "g^")
    plt.xlabel('Abscisse')
    plt.ylabel('Moment')
    #plt.axis([0,340,-10,5])
    plt.grid(True)
    plt.show()


main()  