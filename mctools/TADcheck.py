# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 15:01:41 2018
Version: 1.0
DESCRIPTION:
    After the application of the script 'fendl31_to21.py' this script is used to check
    the differences in total atomic ratio

NOTES:

EXECUTION:
    to execute just change accordingly to your needs the 'pathfile' and 'pathreference'
    variables.

@author: Laghi Davide
"""
import re
import pandas as pd

def TADcheck(pathreference):
    
    idEndMaterial='END OF MATERIAL SECTION'
    patMaterial=re.compile('(?i)m\d+')
    patSpace=re.compile('\s+')
    patComment=re.compile('(?i)c')
    df_rows=[]
    tarList=[]
    matName=''
    flag=False
    
    
    with open(pathreference+'_fendl21.i','r',errors='ignore') as infile:
        for line in infile:
            
            if line.find(idEndMaterial) !=-1:
                flag=False
                sumtar=sum(tarList)
                df_rows.append({'Material':matName, 'TAD FENDL2.1':sumtar})
                
            if patComment.match(line) == None:
                if patMaterial.match(line) != None:
                    matNameOld=matName
                    matName=patMaterial.match(line).group()
                    flag=True
                    sumtar=sum(tarList)
                    df_rows.append({'Material':matNameOld, 'TAD FENDL2.1':sumtar})
                    tarList=[]
                if flag:
                    pieces=patSpace.split(line)
                    try:
                        tar=float(pieces[2])
                    except ValueError:
                        tar=0
                    except IndexError:
                        tar=0
                    tarList.append(tar)
    
    tadfendl31=[]
    with open(pathreference,'r',errors='ignore') as infile:
        for line in infile:
            
            if line.find(idEndMaterial) !=-1:
                flag=False
                sumtar=sum(tarList)
                tadfendl31.append(sumtar)
                
            if patComment.match(line) == None:
                if patMaterial.match(line) != None:
                    matNameOld=matName
                    matName=patMaterial.match(line).group()
                    flag=True
                    sumtar=sum(tarList)
                    tadfendl31.append(sumtar)
                    tarList=[]
                if flag:
                    pieces=patSpace.split(line)
                    try:
                        tar=float(pieces[2])
                    except ValueError:
                        tar=0
                    except IndexError:
                        tar=0
                    tarList.append(tar)
    
    del df_rows[0]
    del tadfendl31[0]
    df=pd.DataFrame(df_rows)
    df['TAD FENDL3.1']=tadfendl31
    df['% deviation']= (df['TAD FENDL2.1']-df['TAD FENDL3.1'])/df['TAD FENDL3.1']
    df.to_excel('logTAD.xlsx')
    
    return;

          