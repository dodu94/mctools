# -*- coding: utf-8 -*-
"""
Created on Wed 13 18:00:00 2019

@author: Marco Fabbri

The aim of this script is to modify the density of the MCNP cell according to the correction factor provided by the external file.
The corrected density are obtained by the multiplication of the density * CF. 
Only the cell listed in the external file are adjusted.
Modified filed writen in a file named as "InputFile + '[Corrected_Density]'".
"""

import re
import numpy as np

def CORRdensity(filename,DensCorr):

    OutputFile=  filename + '[Corrected_Density]'
    OutputLog =  filename + '[LogFile]'
    
    patternMAT  = re.compile('\d')      # Pattern to find the beginning of the material lines
    patternLINE = re.compile('^\s*$')   # Pattern to find the blank lines in the file

    LineBLANK=0
    
    dc=[]      # Density correction matrix
    cells=[]   # Cell No.

    with open(DensCorr, "r", errors="surrogateescape") as infile:
        for line in infile:
            split=line.split()
            cells.append(split[0])
            dc.append(float(split[1]))
            
    # print(cells)
    # print(dc)

    with open(OutputLog,"w", errors="surrogateescape") as outfileLog:
        outfileLog.write('C  '+'The following cells have been modified employing the information provided in '+ DensCorr + ' file !\n')
        outfileLog.write('C  '+'{:^20}'.format('--Cell No.--')+'\t'+'{:^20}'.format('--Former Density--')+'\t'+'{:^20}'.format('-- New Density--')+'\t'+'{:^20}'.format('--Correction factor--') + ' \n')

        with open(OutputFile,"w", errors="surrogateescape") as outfile:
            with open(filename, errors="surrogateescape") as infile:
                for line in infile:
                    
                    LINE = patternLINE.match(line)
                    
                    if LINE:                                   # Finder of line to change the MCNP Input section
                        LineBLANK=LineBLANK+1
                        
                    if LineBLANK==0:                           # Operate only in the material section (the first one)
                        
                        MAT = patternMAT.match(line, 0)
                        if MAT != None :                       # Operate only if material No. is found in the first character of the line
                            split=line.split()
                            
                            value = find_element_in_list(split[0], cells)
                                                    
                            if ((value != None) and ( int(split[1]) != 0)):     # Operate only if the cell is contained in the input provided and not void cells
                                odensity=split[2]                                                    # Former density
                                ndensity=str(round(float(split[2])*float(dc[value]), len(split[2]))) # New density
                                split[2]= ndensity
                                
                                line_MOD=" ".join(split)
                                
                                outfileLog.write('C  '+'{:^20}'.format(split[0])+'\t'+'{:^20}'.format(odensity)+'\t'+'{:^20}'.format(ndensity)+'\t'+'{:^15}'.format(dc[value]) + ' \n')
                                
                                if len(line_MOD)>= 80:         # If the resulting line is > 80 characters wrap after the material density.
                                    pieces=line_MOD.split()
                                    
                                    line_MOD_1=" ".join(pieces[0:7])
                                    line_MOD_2=" ".join(pieces[7:])
                                    
                                    outfile.write(line_MOD_1+'\n')
                                    outfile.write('        '+line_MOD_2+'\n')
                                else:
                                    outfile.write(line_MOD+'\n')
                                del value # To clean the variable
                            else:
                                outfile.write(line)
                        else:
                            outfile.write(line)
                    else:
                        outfile.write(line)
        return;

# if element is found it returns index of element else returns None
def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None