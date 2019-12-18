# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:13:30 2018
Version: 1.0
DESCRIPTION:
    it takes an MCNP input and downgrades from FENDL3.1 to FENDL2.1 libraries

NOTES:
    - All comments in material section are removed
    - Zaids that are not in FENDL2.1 library are commented out

EXECUTION:
    to work it needs the additional excel file that sums up the differences between
    the two libraries (fendlConfront.xlsx).
    to execute just change accordingly to your needs the 'pathfile' and 'pathout'
    variables.

@author: Laghi Davide
"""
import re
import pandas as pd
import os

def fendlDowngrade(pathfile):
    
    idMaterial='MATERIAL SECTION'
    idEndMaterial='END OF MATERIAL SECTION'
    
    patMaterial=re.compile('(?i)m\d+')
    patSpace=re.compile('\s+')
    patComment=re.compile('(?i)c')
    patPoint=re.compile('\.')
    patZaid=re.compile('\.\d\d[A-Za-z]$')
    
    flagMaterial=False
    
    materialBlock=[]
    materialLines=[]
    count=0
    
    # === LOADING LIBRARIES DIFFERENCES ===
    pathdata=os.path.dirname(os.path.abspath(__file__))
    newPathData = os.path.join(pathdata, 'fendlConfront.xlsx')
    df=pd.read_excel(newPathData, index_col=[0])
    fendl21=df.index
    fendl31=df['fendl31'].tolist()
    mode=df['mode'].tolist()
    # === READING MATERIAL SECTION ===
    with open(pathfile,'r', errors="surrogateescape") as infile:
        for line in infile:
            if flagMaterial:
                
                if patComment.match(line):
                    count=count+1#dummy action (placeholder)
                    #materialBlock.append(line)#If the line is a comment is directly added to the block
                else:
                    checkMat=patMaterial.match(line)
                    if checkMat != None:# A new material is found
                        #-----------------------------------------------------------------
                        # === Operate on material lines and than add them to the block ===
                        #-----------------------------------------------------------------
                        index=0
                        newMatLines=[]
                        zaid21mode2=[]
                        zaid21indexes=[]
                        for lineIndex,item in enumerate(materialLines):
                            index=index+1
                            pieces=patSpace.split(item)
                            #DIFFERENT BEHAVIOUR IF THE LINE CONTAINS MATERIAL NAME
                            if index == 1:
                                materialName=pieces[0]
                                zaid31=pieces[1]
                                repetitions=0
                                newMatLines.append(materialName+'\n')
                                #to ensure there is small c
                                zaid31=zaid31[:-1]
                                zaid31=zaid31+'c'
                                if zaid31 in fendl31:#if the line contains zaids
                                    zaidpieces=patPoint.split(zaid31)
                                    des=zaidpieces[1]
                                    if des=='31c':
                                        repetitions=-1
                                        density31=pieces[2]
                                        position=fendl31.index(zaid31)
                                        currentMode=int(mode[position])
                                        zaid21=fendl21[position]
                                        #mode1: direct correspondence between zaids
                                        if currentMode==1:
                                            newLine='        '+zaid21+'   '+density31+'\n'
                                            newMatLines.append(newLine)
                                        #mode2: just one zaid2.1 for multiple zaid3.1 
                                        elif currentMode==2:
                                            density21=float(density31)
                                            zaid21mode2.append(zaid21)
                                            zaid21indexes.append(lineIndex-repetitions)
                                            newLine=[zaid21,density21]#work in progress
                                            newMatLines.append(newLine)
                                        elif currentMode==3:
                                            newLine='c '+item
                                            newMatLines.append(newLine)
                                        else:
                                            print('something went wrong')
                                    else:
                                        newMatLines.append(item)
                                else:
                                    if patZaid.search(zaid31) != None:
                                        del newMatLines[0]
                                        newMatLines.append(item)
                            #NORMAL LINE
                            else:
                                zaid31=pieces[1]
                                #to ensure there is small c
                                zaid31=zaid31[:-1]
                                zaid31=zaid31+'c'
                                density31=pieces[2]
                                zaidpieces=patPoint.split(zaid31)
                                des=zaidpieces[1]
                                if des=='31c':
                                    #Converting to fendl3.2
                                    position=fendl31.index(zaid31)
                                    currentMode=int(mode[position])
                                    zaid21=fendl21[position]
                                    #mode1: direct correspondence between zaids
                                    if currentMode==1:
                                        newLine='        '+zaid21+'   '+density31+'\n'
                                        newMatLines.append(newLine)
                                    #mode2: just one zaid2.1 for multiple zaid3.1 
                                    elif currentMode==2:
                                        density21=float(density31)
                                        if zaid21 not in zaid21mode2:#If the zaid2.1 was still not used 
                                            zaid21mode2.append(zaid21)
                                            zaid21indexes.append(lineIndex-repetitions)
                                            newLine=[zaid21,density21]#work in progress
                                            newMatLines.append(newLine)
                                        else:#The zaid is already used
                                            pos21=zaid21mode2.index(zaid21)
                                            posMat=zaid21indexes[pos21]
                                            repetitions=repetitions+1
                                            try:
                                                newMatLines[posMat][1]=newMatLines[posMat][1]+density21 #The line is modified
                                            except:
                                                print(newMatLines)
                                                print(newMatLines[posMat])
                                    elif currentMode==3:
                                        newLine='c '+item
                                        newMatLines.append(newLine)
                                    else:
                                        print('something went wrong')
                                else:
                                    newMatLines.append(item)
                        materialBlock.append(newMatLines)
                        #-----------------------------------------------------------------
                        ##################################################################
                        #Reset the material lines
                        materialLines=[]
                        materialLines.append(line)
                    else:#if not in a new material keep memorizing isotopes
                        materialLines.append(line)
                
                
            if line.find(idMaterial) !=-1:
                flagMaterial=True
            if line.find(idEndMaterial) !=-1:
                flagMaterial=False
                #-----------------------------------------------------------------
                # === Operate on material lines and than add them to the block ===
                #-----------------------------------------------------------------
                index=0
                newMatLines=[]
                zaid21mode2=[]
                zaid21indexes=[]
                for lineIndex,item in enumerate(materialLines):
                    index=index+1
                    pieces=patSpace.split(item)
                    #DIFFERENT BEHAVIOUR IF THE LINE CONTAINS MATERIAL NAME
                    if index == 1:
                        materialName=pieces[0]
                        zaid31=pieces[1]
                        repetitions=0
                        newMatLines.append(materialName+'\n')
                        #to ensure there is small c
                        zaid31=zaid31[:-1]
                        zaid31=zaid31+'c'
                        if zaid31 in fendl31:#if the line contains zaids
                            zaidpieces=patPoint.split(zaid31)
                            des=zaidpieces[1]
                            if des=='31c':
                                repetitions=-1
                                density31=pieces[2]
                                position=fendl31.index(zaid31)
                                currentMode=int(mode[position])
                                zaid21=fendl21[position]
                                #mode1: direct correspondence between zaids
                                if currentMode==1:
                                    newLine='        '+zaid21+'   '+density31+'\n'
                                    newMatLines.append(newLine)
                                #mode2: just one zaid2.1 for multiple zaid3.1 
                                elif currentMode==2:
                                    density21=float(density31)
                                    zaid21mode2.append(zaid21)
                                    zaid21indexes.append(lineIndex-repetitions)
                                    newLine=[zaid21,density21]#work in progress
                                    newMatLines.append(newLine)
                                elif currentMode==3:
                                    newLine='c '+item
                                    newMatLines.append(newLine)
                                else:
                                    print('something went wrong')
                            else:
                                newMatLines.append(item)
                        else:
                            if patZaid.search(zaid31) != None:
                                del newMatLines[0]
                                newMatLines.append(item)
                    #NORMAL LINE
                    else:
                        zaid31=pieces[1]
                        #to ensure there is small c
                        zaid31=zaid31[:-1]
                        zaid31=zaid31+'c'
                        density31=pieces[2]
                        zaidpieces=patPoint.split(zaid31)
                        des=zaidpieces[1]
                        if des=='31c':
                            #Converting to fendl3.2
                            position=fendl31.index(zaid31)
                            currentMode=int(mode[position])
                            zaid21=fendl21[position]
                            #mode1: direct correspondence between zaids
                            if currentMode==1:
                                newLine='        '+zaid21+'   '+density31+'\n'
                                newMatLines.append(newLine)
                            #mode2: just one zaid2.1 for multiple zaid3.1 
                            elif currentMode==2:
                                density21=float(density31)
                                if zaid21 not in zaid21mode2:#If the zaid2.1 was still not used 
                                    zaid21mode2.append(zaid21)
                                    zaid21indexes.append(lineIndex-repetitions)
                                    newLine=[zaid21,density21]#work in progress
                                    newMatLines.append(newLine)
                                else:#The zaid is already used
                                    pos21=zaid21mode2.index(zaid21)
                                    posMat=zaid21indexes[pos21]
                                    repetitions=repetitions+1
                                    newMatLines[posMat][1]=newMatLines[posMat][1]+density21 #The line is modified
                            elif currentMode==3:
                                newLine='c '+item
                                newMatLines.append(newLine)
                            else:
                                print('something went wrong')
                        else:
                            newMatLines.append(item)
                materialBlock.append(newMatLines)
                #-----------------------------------------------------------------
                ##################################################################
    
    #=== OUTPUT ===    
    with open(pathfile,'r', errors="surrogateescape") as infile , open(pathfile+'_fendl21.i','w', errors="surrogateescape") as outfile:
        del materialBlock[0]
        flag=True
        if flag:
            for line in infile:
                if line.find(idMaterial) != -1:
                    flag=False
                    break
                else:
                    outfile.write(line)
        for block in materialBlock:
            for item in block:
                if isinstance(item,str):
                    outfile.write(item)
                else:
                    outfile.write('        '+item[0]+'   '+str(item[1])+'\n')
        for line in infile:
            if line.find(idEndMaterial) !=-1:
                flag=True
            if flag:
                outfile.write(line)

    return;