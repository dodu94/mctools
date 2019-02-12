# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:37:39 2018

@author: laghida
"""

import numpy as np
import os


principal_menu="""
 ***********************************************
          Process weight window 
 ***********************************************

 * Display WW information   (info)
 * Softening and Scaling    (operate)
 * Plotting to .tif         (plot) 
 * Fill holes in ww         (fillhole)
 * Write the modified ww    (write)
 * Exit the application     (exit)
"""
select_WW = '\nWhich WW do you want to use?'

principalOptions=['info','operate','plot','fillhole','exit', 'write']

def selectWW(wwList):
    while True:
        print(select_WW+' -> '+wwList)
        ww_name = input("\n Select an WW: ")
        if ww_name not in wwList:
            print("Please select a valid ww")
        else:
            break
    return ww_name
        
def clear_screen():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')
    
# --VIEWER--
def loadView(InputFilename,Xs, Xf, Ys, Yf, Zs, Zf, X, Y, Z, X_DIM, Y_DIM, Z_DIM, NoPar, NoERG_P1, NoERG_P2, WW_DIM, WW_P1, WW_P2, WW_E1, WW_E2, wwList):
    clear_screen()
    print(principal_menu)
    
    while True:
        option = input("\n Select an option: ")
        if option not in principalOptions:
            print("Please select a valid option")
        else:
            break
        
    if option == 'info':
        [WW_ANAL_P1, WW_ANAL_P2] = info(InputFilename, Xs, Xf, Ys, Yf, Zs, Zf, X_DIM, Y_DIM, Z_DIM, NoPar, NoERG_P1, NoERG_P2, WW_P1, WW_P2, WW_E1, WW_E2)

    if option == 'plot':
        fileName = selectWW(wwList)
        #select particle
        while True:
            PAR_String = input('\nWhich particle you want to plot?(1=n, 2=p): ' )
            if PAR_String not in ['1','2']:
                print('Please enter a valid particle identifier')
            else:
                PAR_Select=int(PAR_String)
                if (PAR_Select>NoPar):
                    print('Error --> No. particle outside range!')
                else:
                    break
        #select Plane
        while True:
            PLANE = input('\nWhich plane to use for the section?(X/Y/Z): ' )
            if PLANE not in ['X','Y','Z']:
                print('Please enter a valid Plane')
            else:
                break
        #select Quote
        while True:
            PLANE_QUOTE_string = input('\nInsert a quote [cm]: ' )
            PLANE_QUOTE=float(PLANE_QUOTE_string)
            flag, DIM, xlabel, ylabel = checkQuote(PLANE,PLANE_QUOTE,X,Y,Z)
            if flag:
                break
            else:
                print('Quote not valid or out of range!')
    
        plot(fileName, DIM, xlabel, ylabel, WW_DIM , NoERG_P1, NoERG_P2, PAR_Select, WW_P1, WW_P2, Z_DIM, Y_DIM, X_DIM, PLANE)
    
    elif option == 'fillhole':
        WWnew_name, WWnew = HoleFilling(Z_DIM, Y_DIM, X_DIM, Y, X, WW_P1, WW_P2, wwList)
    
#    elif option == 'operate':
#        fileName = selectWW(wwList)
#        soft = input('Please enter a softening factor :')
#        scale = input('Please enter a scaling factor :')
#        operate(Z_DIM, Y_DIM, X_DIM, WW_MOD, soft, scale)
        
    elif option == 'write':
        
        write(wwList[-1],Z_DIM, Y_DIM, X_DIM,Xs,Ys,Zs,Xf,Zf,Yf,WW_P1, WW_P2)
    
    elif option == 'exit':
        exit()
    
    try:
        input("Press enter to select a new option")
    except SyntaxError:
        pass

def nextStep():
    
    while True:
        nextStep = input('\n Do you want to clear the video? (y/n): ' )
        if nextStep not in ['y','n']:
            print('Please answer with "y" or "n"')
        else:
            break
    
    if nextStep == 'y':
        clear_screen()
        

# --LOADING AND READING WW--
def loadWW(InputFilename):

    vector_WW_P1=[]
    vector_WW_P2=[]

    vector_WW_E1=[]
    vector_WW_E2=[]
    
    WW_P2=[]
    WW_E2=[]
    
    NoELEM_P1=0
    NoELEM_P2=0

    NoERG_P1=0
    NoERG_P2=0


    with open( InputFilename, "r") as infile:
        jj=0
        kk=0

        for line in infile:

            if  (jj==0) :
                line=line[:40]

                split=line.split()

                B1_ni=float(split[2])


            elif(jj==1) :
                del split
                split=line.split()

                B1_ne0=float(split[0])

                if (B1_ni==2):
                    B1_ne1=float(split[1])
                else:
                    B1_ne1=0

            elif(jj==2) :
                del split
                split=line.split()

                X_DIM=float(split[0])
                Y_DIM=float(split[1])
                Z_DIM=float(split[2])

                WW_DIM=X_DIM*Y_DIM*Z_DIM

                Xs=float(split[3])
                Ys=float(split[4])
                Zs=float(split[5])

            elif(jj==3) :
                del split
                split=line.split()


            elif(jj==4) :
                del split
                split=line.split()

                Xf=float(split[2])

            elif(jj==5) :
                del split
                split=line.split()

                Yf=float(split[2])

            elif(jj==6) :
                del split
                split=line.split()

                Zf=float(split[2])
                
                X=np.linspace(Xs,Xf,int(X_DIM+1))
                Y=np.linspace(Ys,Yf,int(Y_DIM+1))
                Z=np.linspace(Zs,Zf,int(Z_DIM+1))

            else:

                if (B1_ni==1):
                    if (kk==0):
                        if (NoERG_P1 < B1_ne0):
                            del split

                            split=line.split()
                            NoERG_P1=NoERG_P1+np.size(split)

                            for item in split:
                                vector_WW_E1.append(float(item))

                            WW_E1=np.array(vector_WW_E1)

                            if (NoERG_P1 == B1_ne0):
                                kk=kk+1

                    elif (kk==1):
                        if (NoELEM_P1 < (WW_DIM*B1_ne0)):
                            del split

                            split=line.split()
                            NoELEM_P1=NoELEM_P1+np.size(split)

                            for item in split:
                                vector_WW_P1.append(float(item))   
                elif(B1_ni==2):
                    if (kk==0):
                        if (NoERG_P1 < B1_ne0):
                            del split

                            split=line.split()
                            NoERG_P1=NoERG_P1+np.size(split)

                            for item in split:
                                vector_WW_E1.append(float(item))

                            WW_E1=np.array(vector_WW_E1)

                            if (NoERG_P1 == B1_ne0):
                                kk=kk+1

                    elif (kk==1):
                        if (NoELEM_P1 < (WW_DIM*B1_ne0)):
                            del split

                            split=line.split()
                            NoELEM_P1=NoELEM_P1+np.size(split)

                            for item in split:
                                vector_WW_P1.append(float(item))   
                            
                            if (NoELEM_P1 == WW_DIM*B1_ne0):
                                kk=kk+1
                                
                    elif (kk==2):
                        if (NoERG_P2 < B1_ne1):
                            del split

                            split=line.split()
                            NoERG_P2=NoERG_P2+np.size(split)

                            for item in split:
                                vector_WW_E2.append(float(item))

                            WW_E2=np.array(vector_WW_E2)

                            if (NoERG_P2 == B1_ne1):
                                kk=kk+1

                    elif (kk==3):
                        if (NoELEM_P2 < (WW_DIM*B1_ne1)):
                            del split

                            split=line.split()
                            NoELEM_P2=NoELEM_P2+np.size(split)

                            for item in split:
                                vector_WW_P2.append(float(item))     
            jj=jj+1   

    if (B1_ni==1):
        WW_P1=np.array(vector_WW_P1)  
        WW_P1=WW_P1.reshape(int(B1_ne0),int(WW_DIM))
        
        WW_P2=0
        WW_E2=0
    elif (B1_ni==2):
        WW_P1=np.array(vector_WW_P1)      
        WW_P1=WW_P1.reshape(int(B1_ne1),int(WW_DIM))
                
        WW_P2=np.array(vector_WW_P2)
        WW_P2=WW_P2.reshape(int(NoERG_P2),int(WW_DIM))
    
    wwList = [InputFilename]
    
    return Xs, Xf, Ys, Yf, Zs, Zf, X, Y, Z, X_DIM, Y_DIM, Z_DIM, WW_DIM, B1_ni, B1_ne0, B1_ne1, WW_P1, WW_P2, WW_E1, WW_E2, wwList

#--INFO--
def info(InputFilename, Xs, Xf, Ys, Yf, Zs, Zf, X_DIM, Y_DIM, Z_DIM, NoPAR, NoERG_P1, NoERG_P2, WW_P1, WW_P2, WW_E1, WW_E2):
    
    infolines=[]
    WW_DIM=X_DIM*Y_DIM*Z_DIM
    infolines.append('\nThe following WW file has been analysed:  '+InputFilename+'\n')
    
    Part_A='From'
    Part_B='To' 
    Part_C='No. Bins'
    
    infolines.append('{:>10}'.format('') + '\t'+Part_A.center(15,"-")+'\t'+Part_B.center(15,"-")+'\t'+Part_C.center(15,"-"))
    
    line_X='{:>10}'.format('X -->')  +'\t'+ '{:^15}'.format(Xs)  +'\t'+ '{:^15}'.format(Xf) +'\t'+ '{:^15}'.format(X_DIM)  
    line_Y='{:>10}'.format('Y -->')  +'\t'+ '{:^15}'.format(Ys)  +'\t'+ '{:^15}'.format(Yf) +'\t'+ '{:^15}'.format(Y_DIM) 
    line_Z='{:>10}'.format('Z -->')  +'\t'+ '{:^15}'.format(Zs)  +'\t'+ '{:^15}'.format(Zf) +'\t'+ '{:^15}'.format(Z_DIM)  
    
    infolines.append(line_X)
    infolines.append(line_Y)
    infolines.append(line_Z)
    
    infolines.append('\nThe file contain {0} particle/s on {1} voxels!'.format(int(NoPAR),int(WW_DIM)))
    
    if (NoPAR == 1):
        infolines.append('\n***** Particle No.1 ****')
        infolines.append('Energy[{0}]: {1}'.format(NoERG_P1,WW_E1))
    elif (NoPAR == 2):
        infolines.append('\n***** Particle No.1 ****')
        infolines.append('Energy[{0}]: {1}'.format(NoERG_P1,WW_E1))
        
        infolines.append('\n***** Particle No.2 ****')
        infolines.append('Energy[{0}]: {1}'.format(NoERG_P2,WW_E2))
    
    NoERG_P1= int(NoERG_P1)
    NoERG_P2= int(NoERG_P2)
    
    WW_ANAL_P1=np.zeros((2,NoERG_P1))
    WW_ANAL_P2=np.zeros((2,NoERG_P2))
    
    for i in range (0, NoERG_P1):
        WW_ANAL_P1[0,i]=np.min(WW_P1[i,:])
        WW_ANAL_P1[1,i]=np.max(WW_P1[i,:])
        
    for i in range (0, NoERG_P2):
        WW_ANAL_P2[0,i]=np.min(WW_P2[i,:])
        WW_ANAL_P2[1,i]=np.max(WW_P2[i,:])
    
    Part_A='Upper Energy [MeV]'
    Part_B='Min' 
    Part_C='Max'
    
    infolines.append('\n'+Part_A.center(30,"-")+'\t'+Part_B.center(15,"-")+'\t'+Part_C.center(15,"-"))
    
    if (NoPAR == 1):

        for i in range (0,NoERG_P1):
            infolines.append('{:^30}'.format(WW_E1[i]) + '\t'+ '{:^15}'.format(WW_ANAL_P1[0,i])  +'\t'+ '{:^15}'.format(WW_ANAL_P1[1,i]))
            
    elif (NoPAR == 2):
        
        for i in range (0,NoERG_P1):
            infolines.append('{:^30}'.format(WW_E1[i]) + '\t'+ '{:^15}'.format(WW_ANAL_P1[0,i])  +'\t'+ '{:^15}'.format(WW_ANAL_P1[1,i]))
        
        for i in range (0,NoERG_P2):
            infolines.append('{:^30}'.format(WW_E2[i]) + '\t'+ '{:^15}'.format(WW_ANAL_P2[0,i])  +'\t'+ '{:^15}'.format(WW_ANAL_P2[1,i]))
            
    for line in infolines:
        print(line)
    print('\n')
        
    with open(InputFilename+'_INFO.txt','w') as outfile:
        for line in infolines:
            outfile.write(line)
    
    return WW_ANAL_P1, WW_ANAL_P2

def checkQuote(PLANE,PLANE_QUOTE,X,Y,Z):
    flag=False
    DIM = 0  
    xlabel="X"
    ylabel="Z"
    
    if (PLANE=='X'):
        if (((PLANE_QUOTE > np.max(X)) ) or ( PLANE_QUOTE < (np.min(X)))):
            print('Error --> X dimension outside range!')
        else:
            DIM = (np.abs(X-PLANE_QUOTE)).argmin()
            #vals = WW_PX [:,:, DIM]   # Slice in X  
            xlabel="Y"
            ylabel="Z"
            flag=True
            
    elif (PLANE=='Y'):
        if (((PLANE_QUOTE > np.max(Y)) ) or ( PLANE_QUOTE < (np.min(Y)))):
            print('Error --> Y dimension outside range!')
        else:
            DIM = (np.abs(Y-PLANE_QUOTE)).argmin()
            #vals = WW_PX [:, DIM,:]   # Slice in Y    
            xlabel="X"
            ylabel="Z"
            flag=True
            
    elif (PLANE=='Z'):
        if (((PLANE_QUOTE > np.max(Z)) ) or ( PLANE_QUOTE < (np.min(Z)))):
            print('Error --> Z dimension outside range!')
        else:
            DIM = (np.abs(Z-PLANE_QUOTE)).argmin()
            #vals = WW_PX [PLANE_QUOTE,:,:]  # Slice in Z
            xlabel="X"
            ylabel="Y"
            flag=True
    
    return flag, DIM, xlabel, ylabel
    
# WW Plotting functions
def  plot(InputFilename, DIM, xlabel, ylabel, WW_DIM , NoERG_P1, NoERG_P2, PAR_Select, WW_P1, WW_P2, Z_DIM, Y_DIM, X_DIM, PLANE):
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    
    WW_PX_TOT=[]
    WW_PX=[]

    if (PAR_Select==1):
        WW_PX_TOT=WW_P1.reshape(int(NoERG_P1),int(WW_DIM))
        WW_PX=WW_PX_TOT[int(NoERG_P1)-1,:]

    elif (PAR_Select==2):
        WW_PX_TOT=WW_P2.reshape(int(NoERG_P2),int(WW_DIM))
        WW_PX=WW_PX_TOT[int(NoERG_P2)-1,:]

    WW_PX=WW_PX.reshape(int(Z_DIM),int(Y_DIM),int(X_DIM))
    WW_PX=np.flipud(WW_PX)    
           
    if PLANE == 'X':
        vals = WW_PX [:,:,DIM]   # Slice in X
    elif PLANE == 'Y':
        vals = WW_PX [:,DIM,:]   # Slice in Y
    elif PLANE == 'Z':
        vals = WW_PX [DIM,:,:]   # Slice in Z
        

    mpl.pyplot.imshow(vals, cmap = plt.get_cmap('jet', 1024),norm=colors.LogNorm())           
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar()
    
                
    plt.title(InputFilename+'@'+PLANE+'='+str(DIM)+'cm_'+str(PAR_Select))


    plt.savefig(InputFilename+'_'+PLANE+'='+str(DIM)+'cm_'+str(PAR_Select)+'.tiff')  
    print ('Plot...Done!')

def HoleFilling(Z_DIM, Y_DIM, X_DIM, Y, X, NF_INP, Inputfile, wwList):
    
    import math 
    
    
    Z_DIM = int(Z_DIM)
    Y_DIM = int(Y_DIM)
    X_DIM = int(X_DIM)
    # PR - Evaluation of the WW
    ZONE=np.zeros((Y_DIM,X_DIM))
    
    for j in range (0, Y_DIM):
        for i in range (0, X_DIM):
            if np.absolute(np.arctan(Y[j]/X[i]))<(20/180*math.pi):
                ZONE[j,i]=1
            
    # Modify the WW_OUT with HOLE_FILLING approach
    WW_MOD=np.zeros(np.size(NF_INP))
    WW_MOD=WW_MOD.reshape(Z_DIM,Y_DIM,X_DIM)
    
    WW_OUT=NF_INP.reshape(Z_DIM,Y_DIM,X_DIM)
    
    
    for k in range (2, Z_DIM-2):
        for j in range (2, Y_DIM-2):
            for i in range (2, X_DIM-2):
                if WW_OUT[k,j,i]==0:
                    if ZONE[j,i]==1:
                        BOX=[]
                        BOX=WW_MOD[(k-2):(k+2),(j-2):(j+2),(i-2):(i+2)]
                        No_Values=np.size(np.nonzero(BOX)) 
                            
                        if No_Values>0:
                            del value
                            value=np.sum(np.sum(BOX))/No_Values   
                            WW_MOD[k,j,i]=value
    
    WWnew_name = Inputfile+'_hf'
    wwList.append(WWnew_name)
    
    return WWnew_name, WW_MOD

def operate(Z_DIM, Y_DIM, X_DIM, WW_MOD, soft, scale):

    for k in range (0, Z_DIM):
        for j in range (0, Y_DIM):
            for i in range (0, X_DIM):
                    WW_MOD[k,j,i]=np.power(WW_MOD[k,j,i]*scale, soft)
    
    return WW_MOD
    
def write(outputFileName,Z_DIM, Y_DIM, X_DIM,Xs,Ys,Zs,Xf,Zf,Yf,WW_P1, WW_P2):
    # WW parameters
    # First line
    B1_if=1
    B1_iv=1
    B1_ni=2
    B1_nr=10
    
    # Second line
    B1_ne0=1
    B1_ne1=1
    B1_ne2=0
    
    B1_ne_value=50
    B2_ne_value=50
    
    with open(outputFileName, "w") as outfile:
        
        line_A='{:>10}'.format('{:.0f}'.format(B1_if))
        line_B='{:>10}'.format('{:.0f}'.format(B1_iv))
        line_C='{:>10}'.format('{:.0f}'.format(B1_ni))
        line_D='{:>10}'.format('{:.0f}'.format(B1_nr))  
        outfile.write(line_A+line_B+line_C+line_D+'\n')
        
        line_A='{:>10}'.format('{:.0f}'.format(B1_ne0))
        if B1_ne1>0:
            line_B='{:>10}'.format('{:.0f}'.format(B1_ne1))
        else:
            line_B='{:>10}'.format('')
        if B1_ne2>0:
            line_C='{:>10}'.format('')
        else:
            line_C='{:>10}'.format('')
            
        outfile.write(line_A+line_B+line_C+'\n')  
        
        line_A= '{:>9}'.format('{:.2f}'.format(X_DIM))
        line_B='{:>13}'.format('{:.2f}'.format(Y_DIM))
        line_C='{:>13}'.format('{:.2f}'.format(Z_DIM))
        line_D='{:>13}'.format('{:.2f}'.format(Xs))
        line_E='{:>13}'.format('{:.2f}'.format(Ys))
        line_F='{:>12}'.format('{:.2f}'.format(Zs))
        outfile.write(line_A+line_B+line_C+line_D+line_E+line_F+'    \n')
    
        line_A= '{:>9}'.format('{:.2f}'.format(1))
        line_B='{:>13}'.format('{:.2f}'.format(1))
        line_C='{:>13}'.format('{:.2f}'.format(1))
        line_D='{:>13}'.format('{:.2f}'.format(1))  
        outfile.write(line_A+line_B+line_C+line_D+'    \n')
        
        line_A= '{:>9}'.format('{:.2f}'.format(Xs))
        line_B='{:>13}'.format('{:.2f}'.format(X_DIM))
        line_C='{:>13}'.format('{:.2f}'.format(Xf))
        line_D='{:>13}'.format('{:.2f}'.format(1))  
        outfile.write(line_A+line_B+line_C+line_D+'    \n')
        
        line_A= '{:>9}'.format('{:.2f}'.format(Ys))
        line_B='{:>13}'.format('{:.2f}'.format(Y_DIM))
        line_C='{:>13}'.format('{:.2f}'.format(Yf))
        line_D='{:>13}'.format('{:.2f}'.format(1))  
        outfile.write(line_A+line_B+line_C+line_D+'    \n')
        
        line_A= '{:>9}'.format('{:.2f}'.format(Zs))
        line_B='{:>13}'.format('{:.2f}'.format(Z_DIM))
        line_C='{:>13}'.format('{:.2f}'.format(Zf))
        line_D='{:>13}'.format('{:.2f}'.format(1))  
        outfile.write(line_A+line_B+line_C+line_D+'    \n')
        
        # ********* NEUTRON WW values *********
        outfile.write('{:>13}'.format('{:.0f}'.format(B1_ne_value)) +'\n')
        
        jj=0
        
        for k in range ((Z_DIM-1), -1, -1):
            for j in range (0, Y_DIM):
                for i in range (0, X_DIM):
                    value=WW_P1[k,j,i]
                    if  jj<5: 
                        line_new='{:>13}'.format('{:.5e}'.format(value))
                        outfile.write(line_new)
                        jj=jj+1        
                    else:
                        line_new='{:>13}'.format('{:.5e}'.format(value))
                        outfile.write(line_new)
                        outfile.write('\n')
                        jj=0
    
        # ********* PHOTON WW values *********    
        outfile.write('{:>13}'.format('{:.0f}'.format(B2_ne_value)) +'\n')
        
        jj=0
        
        for k in range ((Z_DIM-1), -1, -1):
            for j in range (0, Y_DIM):
                for i in range (0, X_DIM):
                    value=WW_P2[k,j,i]
                    if  jj<5: 
                        line_new='{:>13}'.format('{:.5e}'.format(value))
                        outfile.write(line_new)
                        jj=jj+1        
                    else:
                        line_new='{:>13}'.format('{:.5e}'.format(value))
                        outfile.write(line_new)
                        outfile.write('\n')
                        jj=0

