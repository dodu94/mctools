# coding: utf-8

'''
LIMITATIONS:
a) only imp, fill, u cards are detected in the line. Further extensions to TRCL card can be easily done.
b) imp card in the format of imp:n, p, e or in the the material sections are not reconized. 
c) line comments between lines are not maintained in the same position.
'''

import re
import numpy as np
import time        # Library to compute time

def WRAP(filename,Flag):

    print('\n Starting .......'+ time.asctime() + '! \n')

    if (Flag == 'tmp') or (Flag == 'dens'):
        FlagMOD = True                                 # Flag to write the modified and wrapped file
        FlagTMP = True                                 # Flag to write the TMP Cell analysis
        if Flag == 'dens':
            FlagMAT_Dens = True                        # Flag to modify the cell material density in function of the U card and of the material 
        else:
            FlagMAT_Dens = False                       # Flag to modify the cell material density in function of the U card and of the material
         
        if Flag == 'tmp':
            FlagU_TMP    = True                        # Flag to modify the TMP card in function of the U card
        else:
            FlagU_TMP    = False                       # Flag to modify the TMP card in function of the U card
    elif Flag == 'tmp_dens':
        FlagMOD = True                                 # Flag to write the modified and wrapped file
        FlagTMP = True 
        FlagMAT_Dens = True  
        FlagU_TMP    = True  
    else:
        FlagMOD      = False
        FlagTMP      = True 
        FlagU_TMP    = False
        FlagMAT_Dens = False 



    # Function to check unique values from list using numpy.unique function
    def unique(array): 
        In = np.array(array) 
        Out = np.unique(In)
        
        return Out;

    # Function to measure the length of a string. To be used when len(str) does not work.
    def lenSTRING(string): 
        len = sum(map(lambda x:1, string))
        
        return len;

    # Function to create the lineCARD of a specific cell
    def cardBUID (tmp, u, fill, IMPn, IMPp, IMPe):
        
        lineCARD = space
        
        if IMPn != '-':
            lineCARD = lineCARD + ' IMP:N='+ IMPn
            
        if IMPp != '-':
            lineCARD = lineCARD + ' IMP:P='+ IMPp
            
        if IMPe != '-':
            lineCARD = lineCARD + ' IMP:E='+ IMPe
            
        if u != '-':
            lineCARD = lineCARD + ' U='+ u

        if tmp != '-':
            lineCARD = lineCARD + ' TMP='+ tmp
            
        if fill != '-':
            if fill[0] == '*':
                lineCARD = lineCARD + '\n' + space + ' *FILL='+ fill[1:]
            else:
                lineCARD = lineCARD + '\n' + space + ' FILL='+ fill[0:]
           
        return lineCARD;
          
    # Function to extract the data from a cell line.    
    def cellANALYSER (line):
        
        split=line.split()

        if (float(split[1]) != 0):             # Operate only if the cell is not a void cell
            CellNo=split[0]
            MatNo =split[1]
            Dens  =split[2]
            
        else:                                  # This is a void cell          
            CellNo=split[0]
            MatNo = '-'
            Dens  = '-' 

        # To search IMP cards
        if (patternIMPn.search(line) != None):
            IMPn = re.search('\d+', line[patternIMPn.search(line).end():]).group()
        else:
            IMPn = '-'
            
        if (patternIMPp.search(line) != None):
            IMPp = re.search('\d+', line[patternIMPp.search(line).end():]).group()
        else:
            IMPp = '-'
            
        if (patternIMPe.search(line) != None):
            IMPe = re.search('\d+', line[patternIMPe.search(line).end():]).group()
        else:
            IMPe = '-'
        
        # To search TMP card
        if (patternTMP.search(line)  != None):
            tmp = re.search(patternEXP, line[patternTMP.search(line).end():]).group()
            tmp = str('{0:1.3E}'.format(float(tmp)))
        else:
            tmp= '-'
            
        # To search Universe card
        if (patternU.search(line)    != None):
            u = re.search('\d+', line[patternU.search(line).end():]).group()
        else:
            u = '-'
            
        # To search FILL card
        if (patternFill.search(line) != None):
            fill = re.search('\d+', line[patternFill.search(line).end():]).group()
            
            # This loop finds the rotation to the fill card if present
            if re.search('\d+(\(|\s+\()', line[patternFill.search(line).end():]) !=None :
                part=line[patternFill.search(line).end():]
                fillROT=part[part.find('('):(part.find(')')+1)]
                
                # This loop avoid to have line with more than 80 characters. Split the () rotation into two lines.
                if len(space + ' ' + fillROT) > 80:
                    fill_split=fillROT.split()
                    for i in range (0, len(fill_split)):
                        if len(space + ' ' + ' '.join(fill_split[:i])) < 80:
                            fillROT  = ' '.join(fill_split[:i]) + '\n' + space + ' ' + ' '.join(fill_split[i:])

                fill = fill + '\n ' + space  + fillROT
                
            
            if line[patternFill.search(line).start()] == '*':
                fill = '*' + fill
        else:
            fill = '-'
        
        # Find where to cut the line
        if patternIMPn.search(line)!= None :
            linePOS.append(patternIMPn.search(line).start())
        if patternIMPp.search(line)!= None :
            linePOS.append(patternIMPp.search(line).start())
        if patternIMPe.search(line)!= None :
            linePOS.append(patternIMPe.search(line).start())
        if patternFill.search(line)!= None :   
            linePOS.append(patternFill.search(line).start())
        if patternTMP.search(line)!= None :
            linePOS.append(patternTMP.search(line).start())
        if patternU.search(line)!= None :
            linePOS.append(patternU.search(line).start())
        
        if linePOS == None:
             POS = lenSTRING(line)
        else:
             POS = min(linePOS)
        
        return CellNo, MatNo, Dens, tmp, u, fill, IMPn, IMPp, IMPe, POS;

    # Function to represent the NOR gate
    def nand (a,b):
        return not (a and b)

    # Function to manage the ValueError response in index for list
    # Return or the index or a None.
    def indexLIST (list, value):
        try:
            i = list.index(value)
        except ValueError:
            i = None 
        else:
            return i

    # filename  = 'C-Model_R181031_rev.i'
    # filename       = 'VV_PS4_S05_C-Model_R190430[ISOLATED]'
    # filename       = 'Sphere_1m_7_N.i'
    # filename       = 'test_1.i'

    filenameMAT_Dens    = 'inputDENS'
    filenameU_TMP       = 'inputTMP'



    if FlagMOD:
        filenameORG    = filename  + '[WRAP-MOD]'
        filenameLOG    = filename  + '[LOG-MOD]'
        filenameTMP    = filename  + '[RESUME-MOD]'
    else:
        filenameORG    = filename  + '[WRAP]'
        filenameLOG    = filename  + '[LOG]'
        filenameTMP    = filename  + '[RESUME]'


    patternComments   = re.compile('C\s+', flags=re.IGNORECASE)
    patternCell       = re.compile('\d+')
    patternNLCell     = re.compile('\s+((\+|\-)\d+|\(|\)|:|\+|\-|\w+|\*|\#)')

    patternLine     = re.compile('^\s*$')   # Pattern to find the blank lines in the file

    patternSpace    = re.compile('\s+|\t+')

    patternNLINE= re.compile('\r\n|\r|\n')
    patternFill = re.compile('(\*|\*\s+|'')FILL(\s+=|=)'  , flags=re.IGNORECASE)
    patternTMP  = re.compile('TMP(\s+=|=)'          , flags=re.IGNORECASE)
    patternU    = re.compile('U(\s+=|=)'            , flags=re.IGNORECASE)
    patternIMPn = re.compile('IMP:n(\s+=|=)'        , flags=re.IGNORECASE)
    patternIMPp = re.compile('IMP:p(\s+=|=)'        , flags=re.IGNORECASE)
    patternIMPe = re.compile('IMP:e(\s+=|=)'        , flags=re.IGNORECASE)
    patternEXP  = r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?"


    TMP_Value  =[]
    TMP_Value_K=[]
    No_Cells   =[]
    Dens_Cells =[]
    MAT_Cells  =[]
    U_Value    =[]
    fill_Value =[]

    IMPn_Value =[]
    IMPp_Value =[]
    IMPe_Value =[]

    Descr_Cells=[]

    space = ' '*5
    linePOS=[]
    lineCARD= space

    wrap       = space
    wrapLINE   = ''
    comments_Value=[]
    Card_Value=[]

    U_List        =[]

    LineBLANK  = 0

    Flag      = False

    u        = None
    tmp      = None
    IMPn     = None
    IMPp     = None
    IMPe     = None
    comments = None
    fill     = None

    lineCARD = space
    wrap     = space
    wrapLINE = ''
    counter  = 0

    print('\n Reading .......'+ filename + '...'+ time.asctime() + '...! \n')

    with open(filenameORG,'w', errors="surrogateescape") as outfile:
        # This loop deals with the MCNP title if present
        with open(filename,'r', errors="surrogateescape", newline='') as infile:
            # Start again the line blank counter
            LineBLANK  = 0
            
            firstLine = infile.readline()
            if nand(patternComments.match(firstLine),patternCell.match(firstLine)):
                outfile.write(firstLine[:firstLine.find('\r')]+'\n')
                
        # This loop extracts and stores the information for the MCNP CELL section
        with open(filename,'r', errors="surrogateescape", newline='') as infile:
            for line in infile:

                LINE = patternLine.match(line)                 # To determine if the line is a blank line.

                if LINE:                                       # Finder to determined the MCNP Input section
                    LineBLANK=LineBLANK+1
                            
                if LineBLANK==0:                               # MCNP Cell Section
                
                    Cell = patternCell.match(line, 0)          # Find the Cell No.
                    
                    if  Cell != None :                         # Starting line of a cell
                                        
                        if (Flag == True):
                            
                            wrapLINE = re.sub('(\r|\n)', ' '  , wrapLINE)
                            wrapLINE = re.sub('\s+', ' '      , wrapLINE)
                            wrapLINE = re.sub('(\s\(\s)', ' (', wrapLINE)
                            wrapLINE = re.sub('(\s\)\s)', ') ', wrapLINE)
                            wrapLINE = re.sub('(\s\:\s)', ':' , wrapLINE)
                            
                            # Extract the information from the cell
                            CellNo, MatNo, Dens, tmp, u, fill, IMPn, IMPp, IMPe, POS = cellANALYSER (wrapLINE)
                                                    
                            wrapLINE=wrapLINE[:(POS)]
                            
                            # Store the cell information in list
                            Descr_Cells.append(wrapLINE)
                            
                            No_Cells.append(CellNo)
                            MAT_Cells.append(MatNo)                    
                            Dens_Cells.append(Dens)
                            
                            IMPn_Value.append(IMPn)
                            IMPp_Value.append(IMPp)
                            IMPe_Value.append(IMPe)
                            
                            Card_Value.append(lineCARD)
                                                    
                            U_Value.append(u)
                            TMP_Value.append(tmp)
                            if tmp != "-":
                                TMP_Value_K.append(str(round(float(tmp)/8.617E-11, 3)))
                            else:
                                TMP_Value_K.append('-')
                            
                            fill_Value.append(fill)
                            
                            if  comments != None :
                                comments_Value.append(comments)
                            else:
                                comments_Value.append('-')
                            
                                                        
                            # Clean variables
                            u        = None
                            tmp      = None
                            IMPn     = None
                            IMPp     = None
                            IMPe     = None
                            comments = None
                            fill     = None

                            lineCARD = space
                            wrap     = space
                            wrapLINE = ''
                            counter  = 0
                            linePOS=[]
                                                            
                        if line.find('$') > 0 :                    
                           
                            if comments == None :
                                comments = line[line.find('$'):line.find('\r')]              # Store  the comments
                            else:
                                comments = comments + line[line.find('$'):line.find('\r')]   # Store  additional comments            
                        
                                            
                        line = line[:line.find('$')]                          # Remove the comments from the line     
                        

                        wrapLINE = line
                        POS=[]
                        Flag      = True
                        
                    elif patternComments.match(line) == None:  # Operate only if the line is not a comment. This could be a additional line of the cell.

                        if line.find('$') > 0 :                    
                           
                            if comments == None :
                                comments = line[line.find('$'):line.find('\r')]                        # Store  the comments
                            else:
                                comments = comments + ' ' + line[line.find('$'):line.find('\r')]   # Store  additional comments          
                        
                            line = line[:line.find('$')]                                               # Remove the comments from the line                 
                                                                
                        if patternNLCell.search(line)!= None:              # A list is considered False if empty else if a True.
                            wrapLINE = wrapLINE + ' ' + line
        
                            POS=[]
                
                else:                                          # All section apart from the Cell one
                    if (Flag == True):                         # This loop is needed to store the information of the last cell
                        
                        wrapLINE = re.sub('(\r|\n)', ' '  , wrapLINE)
                        wrapLINE = re.sub('\s+', ' '      , wrapLINE)
                        wrapLINE = re.sub('(\s\(\s)', ' (', wrapLINE)
                        wrapLINE = re.sub('(\s\)\s)', ') ', wrapLINE)
                        wrapLINE = re.sub('(\s\:\s)', ':' , wrapLINE)
                            
                        CellNo, MatNo, Dens, tmp, u, fill, IMPn, IMPp, IMPe, POS = cellANALYSER (wrapLINE)
                                                
                        wrapLINE=wrapLINE[:(POS)]
                        
                        Descr_Cells.append(wrapLINE)
                        
                        No_Cells.append(CellNo)
                        MAT_Cells.append(MatNo)                    
                        Dens_Cells.append(Dens)
                        
                        IMPn_Value.append(IMPn)
                        IMPp_Value.append(IMPp)
                        IMPe_Value.append(IMPe)
                        
                        Card_Value.append(lineCARD)
                                                
                        U_Value.append(u)
                        TMP_Value.append(tmp)
                        if tmp != "-":
                            TMP_Value_K.append(str(round(float(tmp)/8.617E-11, len(tmp))))
                        else:
                            TMP_Value_K.append('-')
                        
                        fill_Value.append(fill)
                        
                        if  comments != None :
                            comments_Value.append(comments)
                        else:
                            comments_Value.append('-')
                        
                                                   
                        # Clean variables
                        u        = None
                        tmp      = None
                        IMPn     = None
                        IMPp     = None
                        IMPe     = None
                        comments = None
                        fill     = None

                        lineCARD = space
                        wrap     = space
                        wrapLINE = ''
                        counter  = 0
                        linePOS=[]
                                                        
                        Flag = False
                        break
                              

        
        if FlagMOD :          # With modification to the cell card
            if FlagU_TMP:     # Operate when tmp card is modified as function of universe number
                print('\n Modifying the TMP cards.......'+ time.asctime()+'\n')
                u_2MOD=[]
                tmp_2MOD=[]
                mat_2MOD=[]
                
                with open(filenameU_TMP,'r', errors="surrogateescape", newline='') as infile:
                    for line in infile:
                        split = line.split()
                        u_2MOD.append(split[0])
                        tmp_2MOD.append(split[1])
                        mat_2MOD.append(split[2])

                for i in range (0, len(Card_Value)):
                    if indexLIST(u_2MOD,U_Value[i]) != None:

                        index = []
                        # This for cycle serves to identify multiple universe conditions and to operate on all.
                        for position, item in enumerate(u_2MOD):
                            if item == U_Value[i]:
                                index.append(position)

                        for j in range (0, len(index)):
                            if mat_2MOD[index[j]] == '-':             # Operate on all the materials
                                if tmp_2MOD[index[j]] != '-':
                                    TMP_Value_K[i]= tmp_2MOD[index[j]]
                                    TMP_Value[i]  = str('{0:1.3E}'.format(float(TMP_Value_K[i])*8.617E-11))
                                else:                                 # To remove the TMP card from all the universe
                                    TMP_Value_K[i]= '-'
                                    TMP_Value[i]  = '-'
                            else:                           # Operate on only a sub-set of the materials
                                if mat_2MOD[index[j]].find(',')!= -1:
                                    value = mat_2MOD[index[j]].split(',') # Create a list containing all to material to be used
                                else:
                                    value = mat_2MOD[index[j]]            # It is a unique value
                                
                                if indexLIST(value,MAT_Cells[i]) != None: # If the cell of the material is contained in the list use this loop
                                    if tmp_2MOD[index[j]] != '-':
                                        TMP_Value_K[i]= tmp_2MOD[index[j]]
                                        TMP_Value[i]  = str('{0:1.3E}'.format(float(TMP_Value_K[i])*8.617E-11))
                                    else:
                                        TMP_Value_K[i]= '-'
                                        TMP_Value[i]  = '-'
                    Card_Value[i]=cardBUID (TMP_Value[i], U_Value[i], fill_Value[i], IMPn_Value[i], IMPp_Value[i], IMPe_Value[i]) 
                    
            if FlagMAT_Dens:  # Operate when density is modified  as function of universe number, material card No.
                print('\n Modifying the cell material density.......'+ time.asctime()+'\n')
                u_2MOD    =[]
                mat_2MOD  =[]
                fact_2MOD =[]
                
                with open(filenameMAT_Dens,'r', errors="surrogateescape", newline='') as infile:
                    for line in infile:
                        split = line.split()
                        u_2MOD.append(split[0])
                        mat_2MOD.append(split[1])
                        fact_2MOD.append(split[2])
                
                for i in range (0, len(Card_Value)):
                    if indexLIST(u_2MOD,U_Value[i]) != None:

                        index = []
                        # This for cycle serves to identify multiple universe conditions and to operate on all.
                        for position, item in enumerate(u_2MOD):
                            if item == U_Value[i]:
                                index.append(position)

                        for j in range (0, len(index)):
                            if mat_2MOD[index[j]] == '-':                 # Operate on all the materials
                                if  MAT_Cells[i] != '-':
                                    Dens_Cells[i]=float(fact_2MOD[index[j]])*float(Dens_Cells[i])
                                    Dens_Cells[i]=str(Dens_Cells[i])

                            else:                                         # Operate on only a sub-set of the materials
                                if mat_2MOD[index[j]].find(',')!= -1:
                                    value = mat_2MOD[index[j]].split(',') # Create a list containing all to material to be used
                                else:
                                    value = mat_2MOD[index[j]]            # It is a unique value
                                
                                if indexLIST(value,MAT_Cells[i]) != None: # If the cell of the material is contained in the list use this loop
                                    Dens_Cells[i]=float(fact_2MOD[index[j]])*float(Dens_Cells[i])
                                    Dens_Cells[i]=str(Dens_Cells[i])
                    Card_Value[i]=cardBUID (TMP_Value[i], U_Value[i], fill_Value[i], IMPn_Value[i], IMPp_Value[i], IMPe_Value[i])                
                
        else:                 # Without any modification to the cell card only wrapping
            for i in range (0, len(Card_Value)):
                Card_Value[i]=cardBUID (TMP_Value[i], U_Value[i], fill_Value[i], IMPn_Value[i], IMPp_Value[i], IMPe_Value[i]) 
        print('\n Writing .......' + filenameORG +'...'+time.asctime()+ '...\n')
        # This loop write the information of the MCNP CELL section in a structured way leaving unchanged the other sections(e.g. surface and materials ones)
        with open(filename,'r', errors="surrogateescape", newline='') as infile:
        

            # Start again the line blank counter
            LineBLANK  = 0
            for line in infile:

                LINE = patternLine.match(line)                 # To determine if the line is a blank line.

                if LINE:                                       # Finder to determined the MCNP Input section
                    LineBLANK=LineBLANK+1
                            
                if LineBLANK==0:
                
                    Cell = patternCell.match(line, 0)          # Find the Cell No.
                    
                    if  Cell != None :                         # The information are write when the corresponding cell is present
                        
                        value=line[re.search('\d+', line ).start():re.search('\d+', line ).end()]
                        index=No_Cells.index(value)
                        wrapLINE=Descr_Cells[index]
                        
                        # outfile.write ('XXXXX___'+wrapLINE+'\n')
                        
                        pieces  = re.split('(\:|\s|\(|\))',wrapLINE)
                        pieces  = re.split('(\:|\s)'      ,wrapLINE)
                        counter=0
                        
                        # This loop operates only in case of the density modification is turned-on
                        # This loop just substitute the density for no-void cells.
                        if FlagMAT_Dens:
                            if pieces[2] != '0': # Work only on no-void cells.
                                # outfile.write (pieces[0]+'___'+pieces[2]+'___'+pieces[4]+'___'+'\n')
                                pieces[4] = Dens_Cells[index]
                                # outfile.write (pieces[0]+'___'+pieces[2]+'___'+pieces[4]+'___'+'\n')
                        
                        # This loop wrap the cell description if needed
                        if lenSTRING(wrapLINE) < (80-len(space)-2):
                            outfile.write(''.join(pieces) + '\n')
                            
                            wrapL = lenSTRING(wrapLINE)
                        else:
                            for i in range (0,pieces.__len__()):
                                                            
                                if (lenSTRING(wrap +     pieces[i])) < (80-len(space)-2):
                                    wrap    = wrap + pieces[i]
                                    wrapL = i - 1
                                else:
                                    if counter ==0:
                                        outfile.write(wrap[re.search('(\+|\-|\w+|\(|\)|:)',wrap).start():] + '\n')
                                        counter=counter +1
                                    else:
                                        outfile.write(space + re.sub('\s+', ' ', wrap)  + '\n')
                                    
                                    wrapL = i
                                    wrap  = space + pieces[i]
                        # This loops operate the last part of the cell description if it has not been written from the previous one                        
                        if wrapL < (pieces.__len__()-1) :
                            wrapF = ' '.join(pieces[wrapL:])
                            wrapF = ' '.join(pieces[(wrapL-2):])
                            wrapF = re.sub('\s+', ' ', wrapF)
                            wrapF = re.sub('(\s\(\s)', '(', wrapF)
                            wrapF = re.sub('(\s\)\s)', ')', wrapF)
                            wrapF = re.sub('(\s\:\s)', ':', wrapF)
                            
                            if len(wrap) < ((80-len(space)-2)) and re.search('(\+|\-|\w+|\(|\)|:)',wrap) != None:
                                outfile.write(space+ ' ' + wrap[re.search('(\+|\-|\w+|\(|\)|:)',wrap).start():]+'\n')
                                                    
                            if (lenSTRING(wrap +     pieces[i])) < (80-len(space)-2):
                                 wrap    = wrap + pieces[i]
                                 wrapL = i - 1
                            else:
                                 if counter ==0:
                                     outfile.write(wrap[re.search('(\w+|\(|\)|:)',wrap).start():] + '\n')
                                     counter=counter +1
                                 else:
                                     outfile.write(space+ ' '+re.sub('\s+', ' ', wrap)  + '\n')
                                 
                                 wrapL = i
                                 wrap  = space + pieces[i]
                                                     
                        # Write lineCARD in a additional line
                        outfile.write(Card_Value[index] + '\n')
                        
                        # Write  comments (if any) in a additional line
                        if comments_Value[index] != '-' :
                            outfile.write(space +' '+ comments_Value[index] + '\n')
                        
                        # Clean variables
                        wrap     = space
                        wrapLINE = ''
                        counter  = 0
                        
                    elif patternComments.match(line):             # This is comment line
                        outfile.write(line[:line.find('\r')]+'\n')
                else:                                          # All section apart from the Cell one            
                    outfile.write(line[:line.find('\r')]+'\n')
                    
                
    print('\n Writing .......' + filenameLOG + time.asctime()+ '! \n')

    # This loop writes the cells LOG. 
    with open(filenameLOG,'w', errors="surrogateescape") as outfile:
        outfile.write('{:^20}'.format('--Cell No.--')+'\t'+'{:^20}'.format('--Mat No.--')+'\t'+'{:^20}'.format('--Density--')+'\t')
        outfile.write('{:^20}'.format('--TMP[VALUE]--')+'\t'+'{:^20}'.format('--TMP[K]--')+'\t'+'{:^20}'.format('--UNIV--')+'\t')
        outfile.write('{:^15}'.format('--IMP:N--')+'\t'+'{:^15}'.format('--IMP:P--')+'\t'+'{:^15}'.format('--IMP:E--')+'\t  '+'Comments:'+'\n')
        
        for i in range (0, np.size(No_Cells)):
            outfile.write('{:^20}'.format(No_Cells[i])+'\t'+'{:^20}'.format(MAT_Cells[i])+'\t'+'{:^20}'.format(Dens_Cells[i])+'\t')
            outfile.write('{:^20}'.format(TMP_Value[i])+'\t'+'{:^20}'.format(TMP_Value_K[i])+'\t'+'{:^20}'.format(U_Value[i])+'\t')
            outfile.write('{:^15}'.format(IMPn_Value[i])+'\t'+'{:^15}'.format(IMPp_Value[i])+'\t'+'{:^15}'.format(IMPe_Value[i])+'\t  '+comments_Value[i]+'\n')

    # This loop computes and write the TMP analysis. 
    if FlagTMP:
        # Information processing        
        Out=unique(U_Value)
        
        # This loop deletes the '-' for the numpy array vector
        for i in range (0,np.size(Out)):
            if Out[i] == '-':
                Out = np.delete(Out,i)
                break

        lines  = []
        cells  = []
        mats   = []
        dens   = []

        tmp    = []
        tmp_k  = []

        print('\n Writing .......the TMP analysis...'+ time.asctime()+'...! \n')

        with open(filenameTMP,'w', errors="surrogateescape") as outfile:
            for j in range (0, np.size(Out)):
                for i in range (0, np.size(TMP_Value)):
                    if Out[j] == U_Value[i]:
                        
                        lines.append(i)
                        
                        cells.append(int(No_Cells[i]))
                        mats.append((MAT_Cells[i]))
                        dens.append((Dens_Cells[i]))
                        
                        tmp.append(TMP_Value[i])
                        tmp_k.append(TMP_Value_K[i])


                CELLS=np.array(cells)
                TMP    =np.array(tmp)
                TMP_K  =np.array(tmp_k)


                outfile.write('No. Universe: ' + Out[j] +'\n')
                outfile.write('Cell Range  : ' + str(CELLS.min()) + ' - ' + str(CELLS.max()) +'\n')
                outfile.write('Materials   : ' + str(unique(mats)) + '\n')
                outfile.write('Dens        : ' + str(unique(dens)) + '\n')  

                outfile.write('TMP[VALUE]  : ' + str(unique(tmp)) + '\n')
                outfile.write('TMP[K]      : ' + str(unique(tmp_k)) + '\n')    
                outfile.write('--------------------------------------------------------------------------------\n')
                
                lines  = []
                cells  = []
                mats   = []
                dens   = []

                tmp    = []
                tmp_k  = []    
                
        
    print('\n MCTOOLS was performed correctly....' + time.asctime()+ '\n')



