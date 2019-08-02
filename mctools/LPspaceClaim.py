# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:41:53 2018

@author: laghida
"""

import numpy as np
import pandas as pd
import re
 
def LPviewSC(inputList):

    # Input parameters
    R=5 # Radius of the sphere
    LINE=100 # Length of the flight direction
    
    # Definition of variables
    X=[]
    Y=[]
    Z=[]
    
    CosX=[]
    CosY=[]
    CosZ=[]
    
    XL=[]
    YL=[]
    ZL=[]
    
    pointIdentifier   = 'x,y,z coordinates:'
    pointList =[]
    dirList = []
    globalpointList = []
          
    for outp in inputList:
        print('\n'+'Recovering lost particles surfaces and cells in '+outp+' ...'+'\n')
        #-- Getting the surfaces and cells with LP --
        fileAsList = []
        with open(outp,'r', errors="surrogateescape") as infile:
            for line in infile:
                fileAsList.append(line)
                
        for i in range(len(fileAsList)):
            line = fileAsList[i]
            if line.find(pointIdentifier) != -1: #LP in cell
                p = re.findall('-*\d.\d+E[+|-]\d+',line)[0:3]
                p = '   '.join(p)
                pointList.append(p)
                dir = re.findall('-*\d.\d+E[+|-]\d+',fileAsList[i+1])[0:3]
                dir = '   '.join(dir)
                dirList.append(dir)
                if '***' in fileAsList[i-10]:
                    gp = re.findall('-*\d.\d+[+|-]\d+',fileAsList[i-9])[0:6]
                else:
                    gp = re.findall('-*\d.\d+[+|-]\d+',fileAsList[i-10])[0:6]
                try:
                    gp[2]
                    for i in range(len(gp)):
                        gp[i] = gp[i][0:-3]+'E'+gp[i][-3:]
                    gp = '   '.join(gp)
                    globalpointList.append(gp)
                except:
                    globalpointList.append('NO')
    if 'NO' in globalpointList:
        for p in pointList:
            split = p.split()
            X.append(float(split[0]))
            Y.append(float(split[1]))
            Z.append(float(split[2]))
        for d in dirList:
            split = p.split()
            CosX.append(float(split[0]))
            CosY.append(float(split[1]))
            CosZ.append(float(split[2]))
    else:
        for p in globalpointList:
            split = p.split()
            X.append(float(split[0]))
            Y.append(float(split[1]))
            Z.append(float(split[2]))
            CosX.append(float(split[3]))
            CosY.append(float(split[4]))
            CosZ.append(float(split[5]))
    # Checking of imported data
    if (np.size(X)==np.size(CosX)):
        print('Import data...OK!')
    else:
        print('Import data...FAILED!')
                
    # Computation of arrival points 
    for i in range (0, np.size(X)):
        XL.append(X[i]+CosX[i]*LINE)  
        YL.append(Y[i]+CosY[i]*LINE)
        ZL.append(Z[i]+CosZ[i]*LINE)
        
        # L.append(np.power(np.power(XL[i]-X[i],2)+np.power(YL[i]-Y[i],2)+np.power(ZL[i]-Z[i],2),0.5))
    
    # Spaceclaim outfile
    with open( 'POINTS_SpaceClaim.py', "w", errors="surrogateescape") as outfile:  
        for i in range (0,np.size(X)): # Export point as sphere
            string = 'SphereBody.Create(Point.Create(CM(' + str(X[i]) + '), CM(' + str(Y[i]) + '), CM(' + str(Z[i]) + ')),Point.Create(CM(' + str(X[i]+R) + '), CM(' + str(Y[i]) + '), CM(' +  str(Z[i]) + ')))\n' 
            outfile.write(string)
        for i in range (0,np.size(X)): # Export flight direction as liones       
            string = 'SketchLine.Create(Point.Create(CM(' + str(X[i]) + '), CM(' + str(Y[i]) + '), CM(' + str(Z[i]) + ')),Point.Create(CM(' + str(XL[i]) + '), CM(' + str(YL[i]) + '), CM(' +  str(ZL[i]) + ')))\n' 
            outfile.write(string)
            
    print('SpaceClaim Python Script...OK!\n')
    