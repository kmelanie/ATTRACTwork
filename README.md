# ATTRACTwork
The here provided workflow aims to refine the results of rigid body docking. All necessary scripts and software dependencies are included in the project folder (*scripte/run_attract/*) or in the gitHub repository "attract". 

Please note: this workflow is still in developement, changes are added and old files could get removed.

## Installation
NOTE: In the following, bold written terms are variables that have to be adjusted in the configuration file (config_all-cut-rest-attract.sh)

To use the here provided scripts get following dependencies:
- get the [ATTRACT](http://www.attract.ph.tum.de/services/ATTRACT/attract.tgz) source code and follow the installation steps provided in the [online documentation](http://www.attract.ph.tum.de/services/ATTRACT/documentation.html). Save the bin directory to your **ATTRACTDIR**.
- clone this repository and save the run_attract directory to your **SCRIPT_DIR**.

## Input and Result Directories 
- organize your input files (.pdb) in your **INPUT_DIR**: each sample needs to be in an individual directory named by its PDB accession code
- prepare your result directory structure like this: **INPUT_DIR**/results/PDB/coarse_grained/ where "results" specifies your **RESULTS_DIR**  and "PDB" is an individual directory for each sample with PDB accsession code that is in your **INPUT_DIR**. 
- if not provided: prepare coarse grained models. Use this bash command: `python2 $ATTRACTTOOLS/reduce.py --chain A receptor.pdb` or `python2 $ATTRACTTOOLS/reduce.py --chain B ligand.pdb`. 
- move the coarse grained models to the folder **INPUT_DIR**/results/sample/coarse_grained/ and make shure that it contains the following four files:
  - receptorr.pdb,
  - receptorr-refe.pdb
  - ligandr.pdb
  - ligandr-refe.pdb 

## Run 
- adjust in your configuration file (run_attract/config_all-cut-rest-attract.sh) all variables (bold written terms above) according to your pathes. Choose also your desired input parameters:
  - **DISTANCE**: cutoff distance of C-alpha atoms used for selection of flexible amino acids during refinement 
  
  ... and restraining factors stabilizing the natural peptide conformation:
  - **REST_DIHEDRALS**: stabilizes equi-dihedral with force constant. Four dihedrals can be regulated. 
  - **REST_ANGLES**: stabilizes equi-angel with force constant. Four angles can be regulated.
  - **REST_BOND**: stabilizes equi-distance with force constant. One bond can be regulated.

  ... or use the default values.  
- to make various runs using the same dataset but different parameters change the name of your **RESULTS** directory in the configuration file to avoid overwriting of previous results. 
- navigate into your **INPUT_DIR** and run `bash $SCRIPT_DIR/run_all-cut-rest-attract-irmsd.sh` from your command line to use the workflow.




