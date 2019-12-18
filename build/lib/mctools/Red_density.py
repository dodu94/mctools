# -*- coding: utf-8 -*-
"""
Created on Thu AuG 01 12:00:00 2019

@author: Marco Fabbri

The aim of this script is to reduce the density of the MCNP cell by a factor 
given by the user. Modified filed writen in a file named as "InputFile + '[Reduced_Density_DensRed]'".
"""

import re

def REDdensity(filename,DensRed):

    OutputFile=  filename + '[Reduced_Density_'+str(DensRed)+']'
    
    
    patternMAT  = re.compile('\d')      # Pattern to find the beginning of the material lines
    patternLINE = re.compile('^\s*$')   # Pattern to find the blank lines in the file

    LineBLANK=0

    with open(OutputFile,'w', errors="surrogateescape") as outfile:
        with open(filename,'r', errors="surrogateescape") as infile:
            for line in infile:
                
                LINE = patternLINE.match(line)
                
                if LINE:                                   # Finder of line to change the MCNP Input section
                    LineBLANK=LineBLANK+1
                    
                if LineBLANK==0:                           # Operate only in the material section (the first one)
                    
                    MAT = patternMAT.match(line, 0)

                    if MAT != None :                       # Operate only if material No. is found in the first character of the line
                        split=line.split()
                        
                        if (float(split[1]) != 0):         # Operate only if the cell is not a void cell
                            
                            line_MOD=line[0:line.find(split[2])] + '{:.3e}'.format(float(split[2])/DensRed) + line[(line.find(split[2])+len(split[2])):]

                            if len(line_MOD)>= 80:         # If the resulting line is > 80 characters wrap after the material density.
                                pieces=line_MOD.split()
                                
                                line_MOD_1=line[0:line.find(split[2])] + '{:.3e}'.format(float(split[2])/DensRed)
                                line_MOD_2=line[(line.find(split[2])+len(split[2])):]
                                
                                outfile.write(line_MOD_1+'\n')
                                outfile.write('        '+line_MOD_2)
                            else:
                                outfile.write(line_MOD)
                        else:
                            outfile.write(line)
                    else:
                        outfile.write(line)
                else:
                    outfile.write(line)
    return;