# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:20:06 2018

@author: laghida
"""

import re
import pandas as pd

def eeout_tovtk(mode,e):
#-------------------------------------------------
#=============== MULTI MODE ======================
#-------------------------------------------------
    if mode=='multi':
        #
        # === READING FILE ===
        #
        
        #Identifiers
        idNodes='NUMBER OF NODES'
        idTets='NUMBER OF 1st TETS'
        id2Tets='NUMBER OF 2nd TETS'
        idParticlesType='PARTICLE LIST'
        idNodeX='NODES X'
        idNodeY='NODES Y'
        idNodeZ='NODES Z'
        idElem='ELEMENT TYPE'
        idConn='CONNECTIVITY DATA 1ST ORDER TETS ELEMENT ORDERED'
        id2Conn='CONNECTIVITY DATA 2ND ORDER TETS ELEMENT ORDERED'
        idNeighbour='NEAREST NEIGHBOR DATA 1ST ORDER TETS'
        id2Neighbour='NEAREST NEIGHBOR DATA 2ND ORDER TETS'
        # Common patterns
        patNumber=re.compile('\d+')
        patNumberSci=re.compile('[-+]*\d+.\d+E[+-]\d+')
        patSpace=re.compile('\s+')
        patFlux=re.compile('d*4$')
        patHeat=re.compile('d*6$')
        #special patterns
        patTets=re.compile('\d\d+')
        
        #pathfile=input('insert .eeout pathfile')
        pathfileList=e
        
        
        # -- Reading mesh topology --
        print('\nReading mesh Topology...')
        
        for iteration, pathfile in enumerate(pathfileList):
            # -- General Variables --
            numTets=0
            numNodes=0
            particleList=[]
            nodesX=[]
            nodesY=[]
            nodesZ=[]
            #Flags
            readFlag=False    

        
        #-------------------------------------------------
        #=============== FIRST ORDER ======================
        #-------------------------------------------------

        
        with open (pathfile,'r', errors="surrogateescape") as infile:
            for line in infile:
                if line.find(idTets) !=-1:
                    tets=re.findall('\d+',line)
                    if int(tets[1]) > 0:

                        t=5
                        
                        # General infos
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find(idNodes) !=-1:
                                    numNodes=patNumber.search(line).group()
                                if line.find(idTets) !=-1:
                                    numTets=patTets.search(line).group()
                                    break
                                
                                    
                        # Particle type
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if readFlag:
                                        particleList=(patNumber.findall(line))
                                        break
                                    
                                if line.find(idParticlesType) !=-1:
                                        readFlag=True
                        
                        
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagX=False
                            readFlagY=False
                            readFlagZ=False
                            
                            for line in infile:
                        
                                # Reading nodes
                                if readFlagX:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesX.append(float(a.group()))
                            
                                if readFlagY:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesY.append(float(a.group()))
                            
                                if readFlagZ:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesZ.append(float(a.group()))
                                
                                if line.find(idNodeX) !=-1:
                                    readFlagX=True
                                if line.find(idNodeY) !=-1:
                                    readFlagY=True
                                    readFlagX=False
                                if line.find(idNodeZ) !=-1:
                                    readFlagZ=True
                                    readFlagY=False
                                
                                #Reading element type
                                if line.find(idElem) !=-1:
                                    readFlagZ=False
                                
                                
                                
                        #Reading connectivity data
                        cells=[]
                        data=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagCon=False
                            
                            for line in infile:
                                if readFlagCon:
                                    data.append(line)
                                if line.find(idConn) !=-1:
                                    readFlagCon=True
                                if line.find(idNeighbour) !=-1:
                                    readFlagCon=False
                        
                        del data[-1]
                        del data[-1]
                        for string in data:
                            newline=string.strip()
                            substrings=patSpace.split(newline)
                            field = '4 '
                            for substring in substrings:
                                num=int(patNumber.search(substring).group())-1
                                field=field+' '+'{:11d}'.format(num)
                            cells.append(field)
                        
                        #-- Reading edits --
                        print('Reading Edits...')
                        editParticles=[]
                        editUserNumber=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            editsDataFlag=False
                            for line in infile:
                                
                                if editsDataFlag:
                                    strippedline=line.strip()
                                    array=patSpace.split(strippedline)
                                    editParticles.append(array[4])
                                    editUserNumber.append(array[1].strip('-'))
                                    editsDataFlag=False
                                
                                if line.find('EDIT DATA') !=-1:
                                    editsDataFlag=True
                                if line.find('NODES X') !=-1:
                                    break
                        
                        editSETS=[]
                        errorSETS=[]
                        patEditNumber=re.compile('\d+$')
                        n_tally=len(editUserNumber)
                        for editCounter,editNumber in enumerate(editUserNumber):
                            with open (pathfile,'r', errors="surrogateescape") as infile:
                                valuesFlag=False
                                errorFlag=False
                                rightTally=False
                                valuesList=[]
                                errorList=[]
                                for line in infile:
                                    if valuesFlag and rightTally :
                                        strippedline=line.strip()
                                        values=patSpace.split(strippedline)
                                        for value in values:
                                            valuesList.append(value)
                                        if line.find('DATA SETS RESULT SQR TIME BIN')!= -1 or line.find('CENTROIDS X')!= -1 or line.find('DATA OUTPUT PARTICLE')!= -1: #added for no err
                                            if line.find('DATA SETS RESULT SQR TIME BIN')!= -1:
                                                del valuesList[0]
                                                del valuesList[-37:]
                                            if line.find('CENTROIDS X')!= -1:
                                                del valuesList[0]
                                                del valuesList[-9:]
                                            if line.find('DATA OUTPUT PARTICLE')!= -1:
                                                del valuesList[0]
                                                del valuesList[-20:]
                                            editSETS.append(valuesList)

                                            
                                    if errorFlag:
                                        strippedline=line.strip()
                                        errorValues=patSpace.split(strippedline)
                                        for value in errorValues:
                                            errorList.append(value)
                                        if line.find('DATA OUTPUT PARTICLE')!= -1 or line.find('CENTROIDS X')!= -1:
#                                            del valuesList[0]
#                                            del valuesList[-37:]
#                                            editSETS.append(valuesList)
                                            if n_tally==(editCounter+1):
                                                del errorList[0]
                                                del errorList[-9:]
                                                errorSETS.append(errorList)
                                                break
                                            else:
                                                del errorList[0]
                                                del errorList[-20:]
                                                errorSETS.append(errorList)
                                                break
                                    
                                    if line.find('DATA OUTPUT PARTICLE') != -1:
                                        checkName=patEditNumber.search(line).group()
                                        rightTally=(editNumber==checkName)
                                    if line.find('DATA SETS RESULT TIME BIN') != -1:
                                        valuesFlag=True
                                    if line.find('DATA SETS RESULT SQR TIME BIN') != -1 or line.find('CENTROIDS X') != -1 or line.find('DATA OUTPUT PARTICLE')!= -1:
                                        valuesFlag=False
                                    if rightTally:    
                                        if line.find('DATA SETS REL ERROR TIME BIN') != -1:
                                            errorFlag=True
                        
                        #--Read material--
                        materialFlag=False
                        materialsList=[]
                        fieldList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find('CONNECTIVITY DATA') !=-1:
                                    break
                                if materialFlag:
                                    strippedline=line.strip()
                                    matLine=patSpace.split(strippedline)
                                    for mat in matLine:
                                        materialsList.append(mat)
                                if line.find('ELEMENT MATERIAL') !=-1:
                                    materialFlag=True
                        
                        del materialsList[-6:]
                        fieldList.append(materialsList)
                        #--Read Density--
                        densityFlag=False
                        volumeFlag=False
                        densityList=[]
                        volumesList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if densityFlag:
                                    strippedline=line.strip()
                                    densityLine=patSpace.split(strippedline)
                                    for density in densityLine:
                                        densityList.append(density)
                                if volumeFlag:
                                    strippedline=line.strip()
                                    volumeLine=patSpace.split(strippedline)
                                    for vol in volumeLine:
                                        volumesList.append(vol)
                                if line.find('DENSITY') !=-1:
                                    densityFlag=True
                                if line.find('VOLUMES') !=-1:
                                    volumeFlag=True
                                    densityFlag=False
                        
                        del densityList[-8:]
                        fieldList.append(densityList)
                        fieldList.append(volumesList)
                        #
                        # === Writing output ===
                        #
                        for n_edit,editname in enumerate(editUserNumber):
                            patDot=re.compile('.')
                            title=patDot.split(pathfile)
                            outpath=title[0]+'_'+editname+'.vtk'
                            print('writing '+outpath+'...')
                            with open(outpath,'w', errors="surrogateescape") as outfile:
                                #-- Header --
                                outfile.write('# vtk DataFile Version 3.0 \n'+ \
                                              'Original file: '+pathfile+'\n'+ \
                                              'ASCII \n \n')
                                #-- DataSet --
                                
                                #NODES
                                outfile.write('DATASET UNSTRUCTURED_GRID \n'+ \
                                              'POINTS '+str(numNodes)+' float')
                                for n, node in enumerate(nodesX):
                                    outfile.write( '\n'+'{:12.6f}'.format(node)+' '+'{:12.6f}'.format(nodesY[n])+' '+'{:12.6f}'.format(nodesZ[n]))
                                #CELLS
                                outfile.write('\n\nCELLS '+numTets+' '+str(int(numTets)*t)+'\n')
                                for line in cells:
                                    outfile.write(line+'\n')
                                #CELL Type
                                outfile.write('\nCELL_TYPES '+numTets+'\n')
                                for i in range(int(numTets)):
                                    outfile.write('10 \n')
                                #CELL DATA
                                checkflux=patFlux.search(editname)
                                checkheat=patHeat.search(editname)
                                if editParticles[n_edit]=='1':
                                    name='Neutron_'
                                else:
                                    name='Photon_'
                                if checkflux != None:
                                    name=name+'Flux_'+checkflux.group()
                                if checkheat != None:
                                    name=name+'Heating_'+checkheat.group()
                                outfile.write('\nCELL_DATA '+numTets+'\n'+ \
                                              '\nSCALARS '+name+' float 1 \n'+ \
                                              'LOOKUP_TABLE default \n')
                                for item in editSETS[n_edit]:
                                    outfile.write(item+'\n')
                                outfile.write('\nSCALARS '+name+'_ERROR'+' float 1 \n'+ \
                                              'LOOKUP_TABLE default \n')
                                if len(errorSETS)>0:
                                    for item in errorSETS[n_edit]:
                                        outfile.write(item+'\n')
                                else:
                                    x=len(editSETS[n_edit])
                                    for n in range(0,x):
                                        outfile.write('0'+'\n')
                                    print('WARNING: No errors input, errors have been all been assigned "0".')
                                    
                                #FIELD DATA
                                fieldDataNames=['Material','Density','Cell_Volume']
                                for field,fieldDataName in enumerate(fieldDataNames):
                                    outfile.write('\nFIELD FieldData 1\n'+ \
                                                  fieldDataName+' 1 '+numTets+' float\n')
                                    for value in fieldList[field]:
                                        outfile.write(value+'\n')
                                        
#-------------------------------------------------
#=============== SECOND ORDER ======================
#-------------------------------------------------
                                        
                if line.find(id2Tets) !=-1:
                    tets=re.findall('\d+',line)
                    if int(tets[1]) > 0:
                        
                        t=11

                        # General infos
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find(idNodes) !=-1:
                                    numNodes=patNumber.search(line).group()
                                if line.find(id2Tets) !=-1:
                                    numTets=patTets.search(line).group()
                                    break
                                
                                    
                        # Particle type
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if readFlag:
                                        particleList=(patNumber.findall(line))
                                        break
                                    
                                if line.find(idParticlesType) !=-1:
                                        readFlag=True
                        
                        
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagX=False
                            readFlagY=False
                            readFlagZ=False
                            
                            for line in infile:
                        
                                # Reading nodes
                                if readFlagX:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesX.append(float(a.group()))
                            
                                if readFlagY:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesY.append(float(a.group()))
                            
                                if readFlagZ:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesZ.append(float(a.group()))
                                
                                if line.find(idNodeX) !=-1:
                                    readFlagX=True
                                if line.find(idNodeY) !=-1:
                                    readFlagY=True
                                    readFlagX=False
                                if line.find(idNodeZ) !=-1:
                                    readFlagZ=True
                                    readFlagY=False
                                
                                #Reading element type
                                if line.find(idElem) !=-1:
                                    readFlagZ=False
                                
                                
                                
                        #Reading connectivity data
                        cells=[]
                        data=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagCon=False
                            
                            for line in infile:
                                if readFlagCon:
                                    data.append(line)
                                if line.find(id2Conn) !=-1:
                                    readFlagCon=True
                                if line.find(id2Neighbour) !=-1:
                                    readFlagCon=False
                        
                        del data[-1]
                        del data[-1]
                        data2=[]
                        twolines=range(0,len(data),2)
                        for num,line in enumerate(data):
                                if num in twolines:
                                    x=' '.join(data[num:num+2])
                                    data2.append(x)
                        for string in data2:
                            newline=string.strip()
                            substrings=patSpace.split(newline)
                            field = '10 '
                            for substring in substrings:
                                num=int(patNumber.search(substring).group())-1
                                field=field+' '+'{:11d}'.format(num)
                            cells.append(field)
                        
                        #-- Reading edits --
                        print('Reading Edits...')
                        editParticles=[]
                        editUserNumber=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            editsDataFlag=False
                            for line in infile:
                                
                                if editsDataFlag:
                                    strippedline=line.strip()
                                    array=patSpace.split(strippedline)
                                    editParticles.append(array[4])
                                    editUserNumber.append(array[1].strip('-'))
                                    editsDataFlag=False
                                
                                if line.find('EDIT DATA') !=-1:
                                    editsDataFlag=True
                                if line.find('NODES X') !=-1:
                                    break
                        
                        editSETS=[]
                        errorSETS=[]
                        patEditNumber=re.compile('\d+$')
                        n_tally=len(editUserNumber)
                        for editCounter,editNumber in enumerate(editUserNumber):
                            with open (pathfile,'r', errors="surrogateescape") as infile:
                                valuesFlag=False
                                errorFlag=False
                                rightTally=False
                                valuesList=[]
                                errorList=[]
                                for line in infile:
                                    if valuesFlag and rightTally :
                                        strippedline=line.strip()
                                        values=patSpace.split(strippedline)
                                        for value in values:
                                            valuesList.append(value)
                                        if line.find('DATA SETS RESULT SQR TIME BIN')!= -1 or line.find('CENTROIDS X')!= -1 or line.find('DATA OUTPUT PARTICLE')!= -1: #added for no err
                                            if line.find('DATA SETS RESULT SQR TIME BIN')!= -1:
                                                del valuesList[0]
                                                del valuesList[-37:]
                                            if line.find('CENTROIDS X')!= -1:
                                                del valuesList[0]
                                                del valuesList[-9:]
                                            if line.find('DATA OUTPUT PARTICLE')!= -1:
                                                del valuesList[0]
                                                del valuesList[-20:]
                                            editSETS.append(valuesList)
                                            
                                    if errorFlag:
                                        strippedline=line.strip()
                                        errorValues=patSpace.split(strippedline)
                                        for value in errorValues:
                                            errorList.append(value)
                                        if line.find('DATA OUTPUT PARTICLE')!= -1 or line.find('CENTROIDS X')!= -1:
                                            if n_tally==(editCounter+1):
                                                del errorList[0]
                                                del errorList[-9:]
                                                errorSETS.append(errorList)
                                                break
                                            else:
                                                del errorList[0]
                                                del errorList[-20:]
                                                errorSETS.append(errorList)
                                                break
                                    
                                    if line.find('DATA OUTPUT PARTICLE') != -1:
                                        checkName=patEditNumber.search(line).group()
                                        rightTally=(editNumber==checkName)
                                    if line.find('DATA SETS RESULT TIME BIN') != -1:
                                        valuesFlag=True
                                    if line.find('DATA SETS RESULT SQR TIME BIN') != -1 or line.find('CENTROIDS X') != -1 or line.find('DATA OUTPUT PARTICLE')!= -1:
                                        valuesFlag=False
                                    if rightTally:    
                                        if line.find('DATA SETS REL ERROR TIME BIN') != -1:
                                            errorFlag=True
                        
                        #--Read material--
                        materialFlag=False
                        materialsList=[]
                        fieldList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find('CONNECTIVITY DATA') !=-1:
                                    break
                                if materialFlag:
                                    strippedline=line.strip()
                                    matLine=patSpace.split(strippedline)
                                    for mat in matLine:
                                        materialsList.append(mat)
                                if line.find('ELEMENT MATERIAL') !=-1:
                                    materialFlag=True
                        
                        del materialsList[-6:]
                        fieldList.append(materialsList)
                        #--Read Density--
                        densityFlag=False
                        volumeFlag=False
                        densityList=[]
                        volumesList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if densityFlag:
                                    strippedline=line.strip()
                                    densityLine=patSpace.split(strippedline)
                                    for density in densityLine:
                                        densityList.append(density)
                                if volumeFlag:
                                    strippedline=line.strip()
                                    volumeLine=patSpace.split(strippedline)
                                    for vol in volumeLine:
                                        volumesList.append(vol)
                                if line.find('DENSITY') !=-1:
                                    densityFlag=True
                                if line.find('VOLUMES') !=-1:
                                    volumeFlag=True
                                    densityFlag=False
                        
                        del densityList[-8:]
                        fieldList.append(densityList)
                        fieldList.append(volumesList)
                        #
                        # === Writing output ===
                        #
                        for n_edit,editname in enumerate(editUserNumber):
                            patDot=re.compile('.')
                            title=patDot.split(pathfile)
                            outpath=title[0]+'_'+editname+'.vtk'
                            print('writing '+outpath+'...')
                            with open(outpath,'w', errors="surrogateescape") as outfile:
                                #-- Header --
                                outfile.write('# vtk DataFile Version 3.0 \n'+ \
                                              'Original file: '+pathfile+'\n'+ \
                                              'ASCII \n \n')
                                #-- DataSet --
                                
                                #NODES
                                outfile.write('DATASET UNSTRUCTURED_GRID \n'+ \
                                              'POINTS '+str(numNodes)+' float')
                                for n, node in enumerate(nodesX):
                                    outfile.write( '\n'+'{:12.6f}'.format(node)+' '+'{:12.6f}'.format(nodesY[n])+' '+'{:12.6f}'.format(nodesZ[n]))
                                #CELLS
                                outfile.write('\n\nCELLS '+numTets+' '+str(int(numTets)*t)+'\n')
                                for line in cells:
                                    outfile.write(line+'\n')
                                #CELL Type
                                outfile.write('\nCELL_TYPES '+numTets+'\n')
                                for i in range(int(numTets)):
                                    outfile.write('24 \n')
                                #CELL DATA
                                checkflux=patFlux.search(editname)
                                checkheat=patHeat.search(editname)
                                if editParticles[n_edit]=='1':
                                    name='Neutron_'
                                else:
                                    name='Photon_'
                                if checkflux != None:
                                    name=name+'Flux_'+checkflux.group()
                                if checkheat != None:
                                    name=name+'Heating_'+checkheat.group()
                                outfile.write('\nCELL_DATA '+numTets+'\n'+ \
                                              '\nSCALARS '+name+' float 1 \n'+ \
                                              'LOOKUP_TABLE default \n')
                                for item in editSETS[n_edit]:
                                    outfile.write(item+'\n')
                                outfile.write('\nSCALARS '+name+'_ERROR'+' float 1 \n'+ \
                                              'LOOKUP_TABLE default \n')
                                
                                if len(errorSETS)>0:
                                    for item in errorSETS[n_edit]:
                                        outfile.write(item+'\n')
                                else:
                                    x=len(editSETS[n_edit])
                                    for n in range(0,x):
                                        outfile.write('0'+'\n')
                                    print('WARNING: No errors input, errors have been all been assigned "0".')
                                    
                                #FIELD DATA
                                fieldDataNames=['Material','Density','Cell_Volume']
                                for field,fieldDataName in enumerate(fieldDataNames):
                                    outfile.write('\nFIELD FieldData 1\n'+ \
                                                  fieldDataName+' 1 '+numTets+' float\n')
                                    for value in fieldList[field]:
                                        outfile.write(value+'\n')


    
    #-------------------------------------------------
    #=============== SINGLE MODE ======================
    #-------------------------------------------------                                        
    elif mode == 'single':
        #
        # === READING FILE ===
        #
       
        #Identifiers
        idNodes='NUMBER OF NODES'
        idTets='NUMBER OF 1st TETS'
        id2Tets='NUMBER OF 2nd TETS'
        idParticlesType='PARTICLE LIST'
        idNodeX='NODES X'
        idNodeY='NODES Y'
        idNodeZ='NODES Z'
        idElem='ELEMENT TYPE'
        idConn='CONNECTIVITY DATA 1ST ORDER TETS ELEMENT ORDERED'
        id2Conn='CONNECTIVITY DATA 2ND ORDER TETS ELEMENT ORDERED'
        idNeighbour='NEAREST NEIGHBOR DATA 1ST ORDER TETS'
        id2Neighbour='NEAREST NEIGHBOR DATA 2ND ORDER TETS'
        # Common patterns
        patNumber=re.compile('\d+')
        patNumberSci=re.compile('[-+]*\d+.\d+E[+-]\d+')
        patSpace=re.compile('\s+')
        patFlux=re.compile('d*4$')
        patHeat=re.compile('d*6$')
        #special patterns
        patTets=re.compile('\d\d+')
        
        #pathfile=input('insert .eeout pathfile')
        pathfileList=e
        
        numTetsMatrix=[]
        numNodesMatrix=[]
        particleListMatrix=[]
        nodesXMatrix=[]
        nodesYMatrix=[]
        nodesZMatrix=[]
        dataMatrix=[]
        cellsMatrix=[]
        editParticlesMatrix=[]
        editUserNumberMatrix=[]
        editSETSMatrix=[]
        errorSETSMatrix=[]
        fieldListMatrix=[]
        nodes_to_add=-1
        # -- Reading mesh topology --
        print('\nReading mesh Topology...')
        for iteration, pathfile in enumerate(pathfileList):
            # -- General Variables --
            numTets=0
            numNodes=0
            particleList=[]
            nodesX=[]
            nodesY=[]
            nodesZ=[]
            #Flags
            readFlag=False    
        #-------------------------------------------------
        #=============== FIRST ORDER ======================
        #-------------------------------------------------
        with open (pathfile,'r', errors="surrogateescape") as infile:
            for line in infile:
                if line.find(idTets) !=-1:
                    tets=re.findall('\d+',line)
                    if int(tets[1]) > 0:
                        
                        t=5
            
                        # General infos
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find(idNodes) !=-1:
                                    numNodes=patNumber.search(line).group()
                                if line.find(idTets) !=-1:
                                    numTets=patTets.search(line).group()
                                    break
                        numTetsMatrix.append(numTets)
                        numNodesMatrix.append(numNodes)
                                
                                    
                        # Particle type
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if readFlag:
                                        particleList=(patNumber.findall(line))
                                        break
                                    
                                if line.find(idParticlesType) !=-1:
                                        readFlag=True
                        particleListMatrix.append(particleList)
                        
                        
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagX=False
                            readFlagY=False
                            readFlagZ=False
                            
                            for line in infile:
                        
                                # Reading nodes
                                if readFlagX:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesX.append(float(a.group()))
                            
                                if readFlagY:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesY.append(float(a.group()))
                            
                                if readFlagZ:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesZ.append(float(a.group()))
                                
                                if line.find(idNodeX) !=-1:
                                    readFlagX=True
                                if line.find(idNodeY) !=-1:
                                    readFlagY=True
                                    readFlagX=False
                                if line.find(idNodeZ) !=-1:
                                    readFlagZ=True
                                    readFlagY=False
                                
                                #Reading element type
                                if line.find(idElem) !=-1:
                                    readFlagZ=False
                        nodesXMatrix.append(nodesX)
                        nodesYMatrix.append(nodesY)
                        nodesZMatrix.append(nodesZ)
                        
                                
                                
                        #Reading connectivity data
                        cells=[]
                        data=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagCon=False
                            
                            for line in infile:
                                if readFlagCon:
                                    data.append(line)
                                if line.find(idConn) !=-1:
                                    readFlagCon=True
                                if line.find(idNeighbour) !=-1:
                                    readFlagCon=False
                        
                        del data[-1]
                        del data[-1]
                        for string in data:
                            newline=string.strip()
                            substrings=patSpace.split(newline)
                            field = '4 '
                            for substring in substrings:
                                num=int(patNumber.search(substring).group())+nodes_to_add
                                field=field+' '+'{:11d}'.format(num)
                            cells.append(field)
                        
                        dataMatrix.append(data)
                        cellsMatrix.append(cells)
                        nodes_to_add=nodes_to_add+int(numNodes)
                        
                        #-- Reading edits --
                        print('Reading Edits in '+pathfile+'...')
                        editParticles=[]
                        editUserNumber=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            editsDataFlag=False
                            for line in infile:
                                
                                if editsDataFlag:
                                    strippedline=line.strip()
                                    array=patSpace.split(strippedline)
                                    editParticles.append(array[4])
                                    editUserNumber.append(array[1].strip('-'))
                                    editsDataFlag=False
                                
                                if line.find('EDIT DATA') !=-1:
                                    editsDataFlag=True
                                if line.find('NODES X') !=-1:
                                    break
                        editParticlesMatrix.append(editParticles)
                        editUserNumberMatrix.append(editUserNumber)
                        
                        editSETS=[]
                        errorSETS=[]
                        patEditNumber=re.compile('\d+$')
                        n_tally=len(editUserNumber)
                        for editCounter,editNumber in enumerate(editUserNumber):
                            with open (pathfile,'r', errors="surrogateescape") as infile:
                                valuesFlag=False
                                errorFlag=False
                                rightTally=False
                                valuesList=[]
                                errorList=[]
                                for line in infile:
                                    if valuesFlag and rightTally :
                                        strippedline=line.strip()
                                        values=patSpace.split(strippedline)
                                        for value in values:
                                            valuesList.append(value)
                                        if line.find('DATA SETS RESULT SQR TIME BIN')!= -1 or line.find('CENTROIDS X')!= -1 or line.find('DATA OUTPUT PARTICLE')!= -1: #for err & no err
                                            if line.find('DATA SETS RESULT SQR TIME BIN')!= -1:
                                                del valuesList[0]
                                                del valuesList[-37:]
                                            if line.find('CENTROIDS X')!= -1:
                                                del valuesList[0]
                                                del valuesList[-9:]
                                            if line.find('DATA OUTPUT PARTICLE')!= -1:
                                                del valuesList[0]
                                                del valuesList[-20:]
                                            editSETS.append(valuesList)
                                            
                                    if errorFlag:
                                        strippedline=line.strip()
                                        errorValues=patSpace.split(strippedline)
                                        for value in errorValues:
                                            errorList.append(value)
                                        if line.find('DATA OUTPUT PARTICLE')!= -1 or line.find('CENTROIDS X')!= -1:
                                            if n_tally==(editCounter+1):
                                                del errorList[0]
                                                del errorList[-9:]
                                                errorSETS.append(errorList)
                                                break
                                            else:
                                                del errorList[0]
                                                del errorList[-20:]
                                                errorSETS.append(errorList)
                                                break
                                    
                                    if line.find('DATA OUTPUT PARTICLE') != -1:
                                        checkName=patEditNumber.search(line).group()
                                        rightTally=(editNumber==checkName)
                                    if line.find('DATA SETS RESULT TIME BIN') != -1:
                                        valuesFlag=True
                                    if line.find('DATA SETS RESULT SQR TIME BIN') != -1 or line.find('CENTROIDS X') != -1 or line.find('DATA OUTPUT PARTICLE')!= -1:
                                        valuesFlag=False
                                    if rightTally:    
                                        if line.find('DATA SETS REL ERROR TIME BIN') != -1:
                                            errorFlag=True
                        editSETSMatrix.append(editSETS)
                        errorSETSMatrix.append(errorSETS)
                        
                        #--Read material--
                        materialFlag=False
                        materialsList=[]
                        fieldList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find('CONNECTIVITY DATA') !=-1:
                                    break
                                if materialFlag:
                                    strippedline=line.strip()
                                    matLine=patSpace.split(strippedline)
                                    for mat in matLine:
                                        materialsList.append(mat)
                                if line.find('ELEMENT MATERIAL') !=-1:
                                    materialFlag=True
                        
                        del materialsList[-6:]
                        fieldList.append(materialsList)
                        #--Read Density--
                        densityFlag=False
                        volumeFlag=False
                        densityList=[]
                        volumesList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if densityFlag:
                                    strippedline=line.strip()
                                    densityLine=patSpace.split(strippedline)
                                    for density in densityLine:
                                        densityList.append(density)
                                if volumeFlag:
                                    strippedline=line.strip()
                                    volumeLine=patSpace.split(strippedline)
                                    for vol in volumeLine:
                                        volumesList.append(vol)
                                if line.find('DENSITY') !=-1:
                                    densityFlag=True
                                if line.find('VOLUMES') !=-1:
                                    volumeFlag=True
                                    densityFlag=False
                        
                        del densityList[-8:]
                        fieldList.append(densityList)
                        fieldList.append(volumesList)
                        
                        fieldListMatrix.append(fieldList)
                        
    #-------------------------------------------------
    #=============== SECOND ORDER ======================
    #-------------------------------------------------
    
                if line.find(id2Tets) !=-1:
                    tets=re.findall('\d+',line)
                    if int(tets[1]) > 0:
                        
                        t=11
                        
                        # General infos
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find(idNodes) !=-1:
                                    numNodes=patNumber.search(line).group()
                                if line.find(id2Tets) !=-1:
                                    numTets=patTets.search(line).group()
                                    break
                        numTetsMatrix.append(numTets)
                        numNodesMatrix.append(numNodes)
                                
                                    
                        # Particle type
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if readFlag:
                                        particleList=(patNumber.findall(line))
                                        break
                                    
                                if line.find(idParticlesType) !=-1:
                                        readFlag=True
                        particleListMatrix.append(particleList)
                        
                        
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagX=False
                            readFlagY=False
                            readFlagZ=False
                            
                            for line in infile:
                        
                                # Reading nodes
                                if readFlagX:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesX.append(float(a.group()))
                            
                                if readFlagY:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesY.append(float(a.group()))
                            
                                if readFlagZ:
                                    split=patSpace.split(line)
                                    for string in split:
                                        a=patNumberSci.search(string)
                                        if a != None:
                                            nodesZ.append(float(a.group()))
                                
                                if line.find(idNodeX) !=-1:
                                    readFlagX=True
                                if line.find(idNodeY) !=-1:
                                    readFlagY=True
                                    readFlagX=False
                                if line.find(idNodeZ) !=-1:
                                    readFlagZ=True
                                    readFlagY=False
                                
                                #Reading element type
                                if line.find(idElem) !=-1:
                                    readFlagZ=False
                        nodesXMatrix.append(nodesX)
                        nodesYMatrix.append(nodesY)
                        nodesZMatrix.append(nodesZ)
                        
                                
                                
                        #Reading connectivity data
                        cells=[]
                        data=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            
                            # Reading nodes
                            readFlagCon=False
                            
                            for line in infile:
                                if readFlagCon:
                                    data.append(line)
                                if line.find(id2Conn) !=-1:
                                    readFlagCon=True
                                if line.find(id2Neighbour) !=-1:
                                    readFlagCon=False
                        
                        del data[-1]
                        del data[-1]
                        data2=[]
                        twolines=range(0,len(data),2)
                        for num,line in enumerate(data):
                            if num in twolines:
                                x=' '.join(data[num:num+2])
                                data2.append(x)
                        for string in data2:
                            newline=string.strip()
                            substrings=patSpace.split(newline)
                            field = '10 '
                            for substring in substrings:
                                num=int(patNumber.search(substring).group())+nodes_to_add
                                field=field+' '+'{:11d}'.format(num)
                            cells.append(field)
                        
                        dataMatrix.append(data2)
                        cellsMatrix.append(cells)
                        nodes_to_add=nodes_to_add+int(numNodes)
                        
                        #-- Reading edits --
                        print('Reading Edits in '+pathfile+'...')
                        editParticles=[]
                        editUserNumber=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            editsDataFlag=False
                            for line in infile:
                                
                                if editsDataFlag:
                                    strippedline=line.strip()
                                    array=patSpace.split(strippedline)
                                    editParticles.append(array[4])
                                    editUserNumber.append(array[1].strip('-'))
                                    editsDataFlag=False
                                
                                if line.find('EDIT DATA') !=-1:
                                    editsDataFlag=True
                                if line.find('NODES X') !=-1:
                                    break
                        editParticlesMatrix.append(editParticles)
                        editUserNumberMatrix.append(editUserNumber)
                        
                        editSETS=[]
                        errorSETS=[]
                        patEditNumber=re.compile('\d+$')
                        n_tally=len(editUserNumber)
                        for editCounter,editNumber in enumerate(editUserNumber):
                            with open (pathfile,'r', errors="surrogateescape") as infile:
                                valuesFlag=False
                                errorFlag=False
                                rightTally=False
                                valuesList=[]
                                errorList=[]
                                for line in infile:
                                    if valuesFlag and rightTally :
                                        strippedline=line.strip()
                                        values=patSpace.split(strippedline)
                                        for value in values:
                                            valuesList.append(value)
                                        if line.find('DATA SETS RESULT SQR TIME BIN')!= -1 or line.find('CENTROIDS X')!= -1 or line.find('DATA OUTPUT PARTICLE')!= -1: #added for no err
                                            if line.find('DATA SETS RESULT SQR TIME BIN')!= -1:
                                                del valuesList[0]
                                                del valuesList[-37:]
                                            if line.find('CENTROIDS X')!= -1:
                                                del valuesList[0]
                                                del valuesList[-9:]
                                            if line.find('DATA OUTPUT PARTICLE')!= -1:
                                                del valuesList[0]
                                                del valuesList[-20:]
                                            editSETS.append(valuesList)
                                            
                                            
                                    if errorFlag:
                                        strippedline=line.strip()
                                        errorValues=patSpace.split(strippedline)
                                        for value in errorValues:
                                            errorList.append(value)
                                        if line.find('DATA OUTPUT PARTICLE')!= -1 or line.find('CENTROIDS X')!= -1:
                                            if n_tally==(editCounter+1):
                                                del errorList[0]
                                                del errorList[-9:]
                                                errorSETS.append(errorList)
                                                break
                                            else:
                                                del errorList[0]
                                                del errorList[-20:]
                                                errorSETS.append(errorList)
                                                break
                                    
                                    if line.find('DATA OUTPUT PARTICLE') != -1:
                                        checkName=patEditNumber.search(line).group()
                                        rightTally=(editNumber==checkName)
                                    if line.find('DATA SETS RESULT TIME BIN') != -1:
                                        valuesFlag=True
                                    if line.find('DATA SETS RESULT SQR TIME BIN') != -1 or line.find('CENTROIDS X') != -1 or line.find('DATA OUTPUT PARTICLE')!= -1:
                                        valuesFlag=False
                                    if rightTally:    
                                        if line.find('DATA SETS REL ERROR TIME BIN') != -1:
                                            errorFlag=True
                        editSETSMatrix.append(editSETS)
                        errorSETSMatrix.append(errorSETS)
                        
                        #--Read material--
                        materialFlag=False
                        materialsList=[]
                        fieldList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if line.find('CONNECTIVITY DATA') !=-1:
                                    break
                                if materialFlag:
                                    strippedline=line.strip()
                                    matLine=patSpace.split(strippedline)
                                    for mat in matLine:
                                        materialsList.append(mat)
                                if line.find('ELEMENT MATERIAL') !=-1:
                                    materialFlag=True
                        
                        del materialsList[-6:]
                        fieldList.append(materialsList)
                        #--Read Density--
                        densityFlag=False
                        volumeFlag=False
                        densityList=[]
                        volumesList=[]
                        with open (pathfile,'r', errors="surrogateescape") as infile:
                            for line in infile:
                                if densityFlag:
                                    strippedline=line.strip()
                                    densityLine=patSpace.split(strippedline)
                                    for density in densityLine:
                                        densityList.append(density)
                                if volumeFlag:
                                    strippedline=line.strip()
                                    volumeLine=patSpace.split(strippedline)
                                    for vol in volumeLine:
                                        volumesList.append(vol)
                                if line.find('DENSITY') !=-1:
                                    densityFlag=True
                                if line.find('VOLUMES') !=-1:
                                    volumeFlag=True
                                    densityFlag=False
                        
                        del densityList[-8:]
                        fieldList.append(densityList)
                        fieldList.append(volumesList)
                        
                        fieldListMatrix.append(fieldList)


        #
        # === Writing output ===
        #
        #Single VTK mode
        results=pd.DataFrame()

        totalTets=str(sum(list(map(int,numTetsMatrix))))
        totalNodes=str(sum(list(map(int,numNodesMatrix))))
        
        outpath='global.vtk'
        print('writing '+outpath+'...')
        with open(outpath,'w', errors="surrogateescape") as outfile:
            #-- Header --
            outfile.write('# vtk DataFile Version 3.0 \n'+ \
                          'Original file: '+pathfile+'\n'+ \
                          'ASCII \n \n')
            #-- DataSet --
            
            #NODES
            outfile.write('DATASET UNSTRUCTURED_GRID \n'+ \
                          'POINTS '+totalNodes+' float')
            for i, item in enumerate(nodesXMatrix): #for each nodesX set
                for n, node in enumerate(item):#for each x node value in the set
                    outfile.write( '\n'+'{:12.6f}'.format(node)+' '+'{:12.6f}'.format((nodesYMatrix[i])[n])+' '+'{:12.6f}'.format((nodesZMatrix[i])[n]))
            #CELLS
            outfile.write('\n\nCELLS '+totalTets+' '+str(int(totalTets)*t)+'\n')
            for item in cellsMatrix:
                for line in item:
                    outfile.write(line+'\n')
            #CELL Type
            if t==11:
                f='24 '
            else:
                f='10 '
            outfile.write('\nCELL_TYPES '+totalTets+'\n')
            for i in range(int(totalTets)):
                outfile.write(f+'\n')
            #CELL DATA
            outfile.write('\nCELL_DATA '+totalTets+'\n')
            for n_edit,editname in enumerate(editUserNumberMatrix[0]):
                checkflux=patFlux.search(editname)
                checkheat=patHeat.search(editname)
                if editParticles[n_edit]=='1':
                    name='Neutron_'
                else:
                    name='Photon_'
                if checkflux != None:
                    name=name+'Flux_'+checkflux.group()
                if checkheat != None:
                    name=name+'Heating_'+checkheat.group()
                outfile.write('\nSCALARS '+name+' float 1 \n'+ \
                              'LOOKUP_TABLE default \n')
                editsetList=[]
                for editset in editSETSMatrix:
                    for item in editset[n_edit]:
                        editsetList.append(float(item))
                        outfile.write(item+'\n')
                results[name]=editsetList
                
                outfile.write('\nSCALARS '+name+'_ERROR'+' float 1 \n'+ \
                              'LOOKUP_TABLE default \n')
                
                if len(errorSETSMatrix[0]) > 0:
                    errorList=[]
                    for errorset in errorSETSMatrix:
                        for item in errorset[n_edit]:
                            errorList.append(float(item))
                            outfile.write(item+'\n')
                    results[name+'_ERROR']=errorList
                else:
                    x=len(editsetList)
                    errorList=[]
                    for n in range(len(errorList),x):
                        errorList.append(0)
                    for item in errorList:
                        outfile.write(str(item)+'\n')
                    results[name+'_ERROR']=errorList
                    print('WARNING: No errors in edit '+editname+', errors have been all been assigned "0".')
                    
            #FIELD DATA
            fieldDataNames=['Material','Density','Cell_Volume']
            for field,fieldDataName in enumerate(fieldDataNames):
                outfile.write('\nFIELD FieldData 1\n'+ \
                              fieldDataName+' 1 '+totalTets+' float\n')
                fieldList=[]
                for fieldlist in fieldListMatrix:
                    for value in fieldlist[field]:
                        fieldList.append(float(value))
                        outfile.write(value+'\n')
                results[fieldDataName]=fieldList
            results.to_pickle('results.pkl')

    return;