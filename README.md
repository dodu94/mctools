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
	A new version ready for installation has been built
	
INSTALLATION/UPDATING:
	Enter in mctools/dist folder:
	pip install mctools-<version>.tar.gz --user
	
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
			