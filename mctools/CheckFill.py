# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:01:00 2018

@author: laghida

The aim of this script is to read the universe definition of C-model and print to 
console the list of envelope whose fill attribute is ON
"""
import re

def checkFilledUniverses(filename,optFlag):
    patternComments = re.compile('(?i)C\s+')
    patternUniverse = re.compile('\d+')
    patternSpace = re.compile('\s+')
    patternFill = 'FILL='
    patternFill2 = 'fill='
    endUniverse= 'END OF UNIVERSE DEFINITIONS'
    
    FlagMultLine=False
    
    filledUniverses=[]
    
    with open(filename,'r', errors="surrogateescape") as infile:
        for line in infile:
    
            if line.find(endUniverse) != -1: # exit the loop once the universes have all been readed
                break
            
            if patternComments.match(line) == None: # if the line is a comment is ignored
                
                a=patternUniverse.match(line) # Register the Universe curenntly checking
                if a != None:
                    universe_number=a.group()
                
                # Add the previously registered universe if is filled
                if line.find(patternFill) != -1:
                    filledUniverses.append(universe_number)
                # Add the previously registered universe if is filled
                if line.find(patternFill2) != -1:
                    filledUniverses.append(universe_number)
    
    with open('logFilledEnvelopes.txt','w', errors="surrogateescape") as outfile:
        for line in filledUniverses:
            outfile.write(line+'\n')
    
    print('\n The filled envelopes were registered correctly \n')
    
    if optFlag:
        with open(filename,'r', errors="surrogateescape") as infile, open(filename+'_noFillers.i','w', errors="surrogateescape") as outfile:
            for line in infile:
                
                if patternComments.match(line) == None: # if the line is not a comment
                    
                    # Check if the filler is on multiple lines 
                    if FlagMultLine:
                        if patternSpace.match(line) != None:
                            #comment the multiline filler
                            outfile.write('c '+line)
                        else:
                            outfile.write(line)
                            FlagMultLine=False
                            
                    # Comment out the filler
                    elif line.find(patternFill) != -1:
                        outfile.write('c '+line)
                        FlagMultLine=True
                        
                    # Comment out the filler
                    elif line.find(patternFill2) != -1:
                        outfile.write('c '+line)
                        FlagMultLine=True
                        
                    # rewrite the line if no fillers are found    
                    else:
                        outfile.write(line)
                        
                #If it's a comment just rewrite the line
                else:
                    outfile.write(line)
                    FlagMultLine=False
                    
        print('\n All fillers have been commented out \n')
    
    else:
        print('\n Fillers were not changed \n')
                    
                    
    
    return;
