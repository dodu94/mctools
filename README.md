# mctools package

This is a package grouping a set of useful tools to edit/extract informations from MCNP input and output files.
The modes that operate on MCNP input files were tested with c-model input file structure, in case they use unique 
identifiers to work (already contained in c-model structure) these identifiers are signaled in the documentation and
should be added to the input file.

BUILDING A NEW VERSION:
	1) Install proper tools, from command line execute:
		'python -m pip install --user --upgrade setuptools wheel'
	2) Go to mctools/mctools: add new scripts and modify main.py accordingly if necessary 
	3) Go to mctools parent folder
	4) Open 'setup.py'.
	5) Modify the version number in the variable 'version' and save.
	6) Go to the same folder where setup.py is located and from command line execute:
		'python setup.py sdist bdist_wheel'
	A new version ready for installation has been built and stored in the "dist" folder.
	
INSTALLATION/UPDATING:
	Enter in mctools/dist folder:
	pip install mctools-<version>.tar.gz --user
	The correspondent version of mctools will be installed and the libraries copied into Pyhton36/site-packages the folder.
	***Please be aware that the content of the mctools/mctools is neither updated nor modified by the installation***
	
GENERAL EXECUTION:
python -m mctools --mode <mode name> -<options> <option value/s>

MODES:
Here is a description of all the modes available, the options with a DEFAULT choice are OPTIONAL:

1) 'tovtk' (DEFAULT): it is used to convert one or more .eeout files in .vtk format.
	
	ADDITIONAL OPTIONS:
		' -opt <single/multi> '
			'single'(default): takes a list of .eeout (or a single one) and generates a unique global.vtk file containing all the infos.
							   In this mode the script also generates a results.pkl file to operate with python pandas dataframes.
			'multi': given a single .eeout generates a .vtk for every edit contained in it
		
		' -e <nomefile1.eeout> <nomefile2.eeout> <nomefile3.eeout> <...> '
			this argument is REQUIRED and consist in the list of the .eeout files to convert
	
	RESTRICTIONS:
		Admitted mesh elements: first order tetra.
		Admitted particles: n,p
		Admmitted edits: 4,6


2) 'lpdebug': The script reads a MCNP output and relative input of a void test and then outputs an Excel file containing the surfaces,cells 
              and filler where the particles were lost. In addition it provides:
			  - A summary listing the most problematic cell for each envelope and calculates an estimation of the intersection area (IA).
			  - A python script that if imported in SpaceClaim allows to visualize the lost particles locations 
	
	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file
		
		' -olist <outputfile1> <outputfile2> ...'
			insert all the MCNP outputs of the same run (it works with continous runs)
		
		' -optlp <spherical/arbitrary/run>
			'spherical' (default): A spherical source was used in a void run, there is no need for the user to give additional details.
			'arbitrary' : An arbitrary source was used in a void run. The user will be requested to enter the area of the source in [cm] in order to be able to 
				         evaluate the Intersection Area.
			'run' : a normal run is considered. The IA cannot be evaluated.
				   
	RESTRICTIONS:
		It does not work for inputs where cells are not inserted in universes.
		

3) 'chkfill': it is used to check which envelopes are filled in the MCNP input and eventually comment them out. It prints a log containig
    the list of filled envelopes.

	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file to check
		
		' -comment <'yes'/'no'> 
			'yes': Creates an input with all fillers commented out.
			'no' (default): No additional action is performed.
	
	UNIQUE IDENTIFIERS:
		'END OF UNIVERSE DEFINITIONS': This needs to be put at the end of the envelope definitions


4) 'fendldown': it is used to downgrade from FENDL3.1 to FENDL2.1 libraries for compatibility purposes. In addition it creates a log where a total
			    atomic density confront is made between the original file and the downgraded one.

	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file to downgrade
	
	UNIQUE IDENTIFIERS:
		'MATERIAL SECTION': this has to be placed at the beginning of the material section
		'END OF MATERIAL SECTION': This has to be placed at the end of the material section
	
	RESTRICTIONS:
		The majority of the comments contained in the material section will be eliminated
		Often in the c-model there are two 'END OF MATERIAL SECTION' comment lines. The one in middle MUST be canceled for the script to work.

4) 'rd':  it is to reduce the density of the MCNP cell by a factor given by the user. Modified filed written in a file named as "InputFile + '[Reduced_Density]'".

	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file to employ
		' -factor <reduction factor> '
			insert the density reduction factor
	
	UNIQUE IDENTIFIERS:
		Not used. MCNP native sections are used.
		
	RESTRICTIONS:
		Only "int" density reduction factor is accepted.
		
4) 'cd':  To multiply the MCNP cell density by a factor given in an external file. 
          Only the cells listed in the external file are modified. 
		  Modified file written in a file named as "InputFile + '[Corrected_Density]'".
		  Log file written in a file named as "InputFile + '[LogFile]'".

	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file to employ
		' -cf <correction factor> '
			File containing the MCNP cells to be modified (first column) and the correspondent correction factor (second column)
	
	UNIQUE IDENTIFIERS:
		Not used. MCNP native sections are used.
		
	RESTRICTIONS:
		No one.

5) 'wrap':  Standard organization of the cell description which spans within the 80 characters. 
            Surface and card sections are not modified. 
			The cell description is followed by a line containing all the cell cards, 
			hence by the fill card with the rotation (if present) than the in-line comments in the subsequent line (if present).  
			Comments are maintained. All the comments present are collected. The organized file is coded as filename + [WRAP]. 
	        The cells’ information collected are properly reported and resumed in file as filename + [RESUME].
            The information of each cell is also written in a table format in a log file which can be easily imported in Excel for further analysis.
			The organized file is coded as filename + [LOG]. 
 
	ADDITIONAL OPTIONS:
		' -i <inputfile> '
			insert the MCNP input file to employ
		' -mod tmp '
			To modify the TMP card of cells according to the information provided in InputTMP.
			Suffix MOD added in output file.
		' -mod dens '
			To modify the cells' density according to the information provided in InputDENS.
			Suffix MOD added in output file.
		' -mod tmp_dens '
			tmp and dens mode together.
	
	UNIQUE IDENTIFIERS:
		Not used. MCNP native sections are used.
		
	RESTRICTIONS:
		No one.		