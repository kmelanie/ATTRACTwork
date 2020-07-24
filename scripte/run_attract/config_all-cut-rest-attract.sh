###
# CONFIG FILE for ATTRACT workflow
###

## runScript directory
SCRIPT_DIR=/home/melaniekaser/attract-master/generat/work/scripte/run_attract
STEPS=$SCRIPT_DIR/steps
## ATTRACT script directory
ATTRACTDIR=/home/melaniekaser/attract-master/bin



## INPUT PARAMETERS (default)
# define the distance used for flexible domain selection (value in Angstrom)
DISTANCE=10
# define restraining factors of dihedrals, angles and bond
REST_DIHEDRALS='[[3.1415, 60.1], [0, 60.1], [1.0, 0.51], [-2.4, 2.1]]'
REST_ANGLES="[[2.02,55.1],[2.13,55.1],[2.13,55.1],[2.09,55.1]]"
REST_BOND='[[1.35, 300.1]]'

## Input/Output directory
INPUT_DIR=/home/melaniekaser/attract-master/generat/work/benchmark5_attract_models
 

RESULTS_DIR=/home/melaniekaser/attract-master/generat/work/benchmark5_attract_models/results
RESULTS=/cutted_distance${DISTANCE}_resttest


