# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:11:15 2018

@author: Laghi Davide

V 1.0

The script reads a MCNP output and relative input and than outputs an Excel
file containing the surfaces and cells where the particles were lost and their universe.
In addition it provides a summary listing the most problemtaic cell for each universe.
"""
import re
import pandas as pd

def lpdebug_normalRun(olist,input_model):

    #-- Identifiers --
    surfaceIdentifier = 'currently being tracked has reached surface'
    cellIdentifier    = 'other side of the surface from cell'
    pointIdentifier   = 'x,y,z coordinates:'
    #-- Patterns --
    Number = re.compile('\d+')
    patComments = re.compile('(?i)C\s+')
    patUniverse = re.compile('(?i)u=\d+')
    patNPS=re.compile('(?i)nps')
    patNPS_value=re.compile('\s+[eE.0-9]+\s*')
    patXYZ=re.compile('\s+[eE.0-9]+\s[eE.0-9]+\s[eE.0-9]+\s*')
    patSDEF = re.compile('(?i)sdef')
    patSDEFsur = re.compile('(?i)sur=\d+')
    
    #-- Variables --
    surfList=[]
    cellList=[]
    pointList=[]
    globalpointList=[]
    universeList=[]
    Trigger=False
    
    for outp in olist:
        print('\n'+'Recovering lost particles surfaces and cells in '+outp+' ...'+'\n')
        #-- Getting the surfaces and cells with LP --
        fileAsList = []
        with open(outp,'r') as infile:
            for line in infile:
                fileAsList.append(line)
                
        for i in range(len(fileAsList)):
            line = fileAsList[i]
            if line.find(surfaceIdentifier) != -1: #LP in surface
                surfList.append(Number.search(line).group())
            if line.find(cellIdentifier) != -1: #LP in cell
                cellList.append(Number.search(line).group())
            if line.find(pointIdentifier) != -1: #LP in cell
                p = re.findall('-*\d.\d+E[+|-]\d+',line)[0:3]
                p = '   '.join(p)
                pointList.append(p)
                if '***' in fileAsList[i-10]:
                    gp = re.findall('-*\d.\d+[+|-]\d+',fileAsList[i-9])[0:3]
                else:
                    gp = re.findall('-*\d.\d+[+|-]\d+',fileAsList[i-10])[0:3]
                try:
                    gp[2]
                    for i in range(len(gp)):
                        gp[i] = gp[i][0:-3]+'E'+gp[i][-3:]
                    gp = '   '.join(gp)
                    globalpointList.append(gp)
                except:
                    globalpointList.append('NO')

    #-- Counting multiple occurrencies --
    organizer=pd.DataFrame(surfList,cellList).reset_index()
    organizer.rename(columns={'index':'Cell',0:'Surface'},inplace=True)
    organizer = organizer.assign(Position=pointList)
    organizer = organizer.assign(GlobalPosition=globalpointList)
    organized = organizer.groupby(organizer.columns.tolist()).size().reset_index().rename(columns={0:'Count'})
    cellListReduced=organized['Cell'].tolist()
    
    print('Assigning surfaces and cells to their filler universe...'+'\n')
    #-- Assign surfaces and cells to their filler universe --
    for cell in cellListReduced:
        with open(input_model,'r', errors='ignore') as infile: # errors='ignore' is due top the fact that in some cases
            for line in infile:                                # there are char in comments that cannot be read
                
                #if the cell is found, the universe search is triggered
                if re.compile(cell).match(line) != None:
                        Trigger = True  
                
                if patComments.match(line) == None: # if the line is a comment is ignored
                    #The universe is registered and the search is stop                
                    if Trigger:
                        u = patUniverse.search(line)
                        if u != None:
                            uNum=Number.search(u.group())
                            Trigger = False
                            universeList.append(uNum.group())
                            break
    
    print('Creating output...'+'\n')
    #-- OUTPUT RESULTS --
    # Cleaning and operating on raw data
    organized['Filler Universe']=universeList
    df_sorted=organized.sort_values(by=['Filler Universe','Count'])
    df_sorted.set_index(["Filler Universe",'Cell','Surface','Position','GlobalPosition'],inplace=True)
    df_max=df_sorted.groupby('Filler Universe').tail(1)
    df_max.reset_index(level=['Cell','Surface','Position','GlobalPosition'],inplace=True)
    df_sum=df_sorted.groupby('Filler Universe').sum()
    df_max['Total LP in universe']=df_sum['Count']
    df_max=df_max.drop(columns='Position')  # Deleting the column Position
    df_max=df_max.drop(columns='GlobalPosition')
    
    #-- Creating Excel Writer Object from Pandas -- 
    writer = pd.ExcelWriter('LPdebug.xlsx',engine='xlsxwriter')   
    workbook=writer.book
    worksheet=workbook.add_worksheet('LP Debugging')
    writer.sheets['LP Debugging'] = worksheet
    worksheet.set_column('A:E',20)
    worksheet.set_column('L:Q',20)
    worksheet.set_column('Q:Q',20)
    worksheet.write('A1', 'LOST PARTICLE LOCATIONS')
    worksheet.write('L1','SUMMARY FOR MOST PROBLEMATIC CELL IN EACH UNIVERSE')
    
    df_sorted.to_excel(writer,sheet_name='LP Debugging',startrow=1 , startcol=0)   
    df_max.to_excel(writer,sheet_name='LP Debugging',startrow=1, startcol=11)
    
    writer.save()
    print('Done!')
    return;