# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:59:54 2018

@author: Laghi Davide
"""

import argparse as ap
#mctools modules import
from mctools import eeoutTOvtk as vtk
from mctools import CheckFill as cf
from mctools import LPdebugger as lp
from mctools import LPdebugger_arbitrarySource as lpa
from mctools import fendl31_to21 as fndl
from mctools import TADcheck as tad
from mctools import LPdebugger_normalRun as lp_nr
from mctools import LPspaceClaim as lp_sc
from mctools import WW_operator as ww
from mctools import Red_density  as rd
from mctools import Corr_density as cd
from mctools import wrap as wr

# Selectable Modes
modes=('tovtk','chkfill','lpdebug','fendldown','ww','rd','cd','wrap')

#--- Parsing ---
descrmode='Convert one or multiple .eeout files in .vtk format'
epi='Specify the "mode" you want to use'

parser = ap.ArgumentParser(prog='mctools',description=descrmode,epilog=epi)
parser.add_argument('--mode', help='Execution mode, "tovtk" by default',
                    type=str,
                    choices=modes,
                    default='tovtk')
# General options
parser.add_argument('-i',help='insert MCNP input file',
                    type=str,
                    default='')
parser.add_argument('-o',help='insert MCNP output file',
                    type=str,
                    default='')
parser.add_argument('-olist',nargs='+', help='list of MCNP outputs',
                    type=str,
                    default=[])
# tovtk
parser.add_argument('-opt', help='"single" (default) for a single .vtk file. "multi" for a .vtk for each edit',
                   type=str,
                   choices=['single','multi'],
                   default='single')
parser.add_argument('-e',nargs='+', help='list of .eeout to convert',
                    type=str,
                    default=[])
# lpdebug
parser.add_argument('-optlp', help='"spherical" (default), if you used a spherical source, "arbitrary" if you did not on a void run. \
                    "run" if you are testing with materials',
                   type=str,
                   choices=['spherical','arbitrary','run'],
                   default='spherical')
# chkfill
parser.add_argument('-comment', help='"yes" if you want to comment out all the fillers. "no" (default) if you do not',
                   type=str,
                   choices=['yes','no'],
                   default='no')
# rd
parser.add_argument('-factor', help='Insert the reduce density factor',
                   type=float)

# cd
parser.add_argument('-cf', help='Insert the name of the file containing the correction factors',
                   type=str)
   
# wrap: mod
parser.add_argument('-mod', help='Insert the type of file wrap modification',
                   type=str)

args=parser.parse_args()

def main():
    # === TOVTK ===
    if args.mode=='tovtk':
        vtk.eeout_tovtk(args.opt,args.e)
    # === CHKFILL ===
    elif args.mode=='chkfill':
        if args.comment=='yes':
            cf.checkFilledUniverses(args.i, True)
        else:
            cf.checkFilledUniverses(args.i, False)
    # == LPDEBUG ==
    elif args.mode=='lpdebug':
        if args.optlp=='spherical':
            lp.lpdebug(args.olist,args.i)
            print('\n Creation of SpaceClaim script\n')
            lp_sc.LPviewSC(args.olist)
        elif args.optlp=='arbitrary':
            lpa.lpdebug_arbitrary(args.olist,args.i)
            print('\n Creation of SpaceClaim script\n')
            lp_sc.LPviewSC(args.olist)
        else:
            lp_nr.lpdebug_normalRun(args.olist,args.i)
            print('\n Creation of SpaceClaim script\n')
            lp_sc.LPviewSC(args.olist)
    # === FENDLDOWN ===
    elif args.mode=='fendldown':
        fndl.fendlDowngrade(args.i)
        tad.TADcheck(args.i)
    # === WW ===
    elif args.mode=='ww':
        print('\n ============ LOADING ==========')
        #load ww
        [Xs, Xf, Ys, Yf, Zs, Zf, X, Y, Z, X_DIM, Y_DIM, Z_DIM, WW_DIM, NoPar, NoERG_P1, NoERG_P2, WW_P1, WW_P2, WW_E1, WW_E2, wwList] = ww.loadWW(args.i)
        
        while True:
            ww.loadView(args.i,Xs, Xf, Ys, Yf, Zs, Zf, X, Y, Z, X_DIM, Y_DIM, Z_DIM, NoPar, NoERG_P1, NoERG_P2, WW_DIM, WW_P1, WW_P2, WW_E1, WW_E2)
        
        
    elif args.mode=='rd':
        rd.REDdensity(args.i,args.factor)

    elif args.mode=='cd':
        cd.CORRdensity(args.i,args.cf)    

    elif args.mode=='wrap':
        wr.WRAP(args.i,args.mod) 

    else:
        print('\nSomething went wrong =(')
        

if __name__ == '__main__':
    main()
