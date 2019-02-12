# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:41:53 2018

@author: laghida
"""

import numpy as np


# Search inside the output files
def outpReader(InputFile,X,Y,Z,CosX,CosY,CosZ):
    # Definition of variables
    
    # Definition of patterns to search
    STRING_A= "x,y,z coordinates:"
    STRING_B= "u,v,w direction cosines:"
    
    
    
    with open(InputFile, "r") as infile:
        for line in infile:
            
            if line.find(STRING_A)!= -1:
                
                line=line[26:]
                split=line.split()
                
                X.append(float(split[0]))
                Y.append(float(split[1]))
                Z.append(float(split[2]))
                
            if line.find(STRING_B)!= -1:
                
                line=line[26:]
                split=line.split()
                
                CosX.append(float(split[0]))
                CosY.append(float(split[1]))
                CosZ.append(float(split[2]))
                    
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
    
    #Check if inputList is a single file or actually a list
    if type(inputList) == list:
        for outp in inputList:
            outpReader(outp,X,Y,Z,CosX,CosY,CosZ)
    else:
        outpReader(inputList,X,Y,Z,CosX,CosY,CosZ)
            
 
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
    with open( 'POINTS_SpaceClaim.py', "w") as outfile:  
        for i in range (0,np.size(X)): # Export point as sphere
            string = 'SphereBody.Create(Point.Create(CM(' + str(X[i]) + '), CM(' + str(Y[i]) + '), CM(' + str(Z[i]) + ')),Point.Create(CM(' + str(X[i]+R) + '), CM(' + str(Y[i]) + '), CM(' +  str(Z[i]) + ')))\n' 
            outfile.write(string)
        for i in range (0,np.size(X)): # Export flight direction as liones       
            string = 'SketchLine.Create(Point.Create(CM(' + str(X[i]) + '), CM(' + str(Y[i]) + '), CM(' + str(Z[i]) + ')),Point.Create(CM(' + str(XL[i]) + '), CM(' + str(YL[i]) + '), CM(' +  str(ZL[i]) + ')))\n' 
            outfile.write(string)
            
    print('SpaceClaim Python Script...OK!\n')
    