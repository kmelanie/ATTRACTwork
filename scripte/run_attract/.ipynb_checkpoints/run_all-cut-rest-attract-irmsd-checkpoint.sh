#!/usr/bin/env sh
##
# Melanie Käser
# T38 - July 2020
#
# Run ATTRACT (see https://github.com/glennclarence/attract)
# GitHub project: ATTRACTwork (see https://github.com/kmelanie/ATTRACTwork)
##

##
# This is a pipeline for optimizing docking positions of simulated protein-protein complexes 
# by creating coarse grained models with flexible but restrained amino acides at the interaction site 
# using the functionality of ATTRACT. 
##


#
# Load the parameters
#

source /home/melaniekaser/attract-master/generat/work/scripte/run_attract/config_all-cut-rest-attract.sh

cd $INPUT_DIR/

for d in [1-9]*/; do

        echo "$d"

	###cut
        mkdir -p $RESULTS_DIR/"$d"/$RESULTS
        python $STEPS/all_coarse-grained_findandcut_script.py $RESULTS_DIR/$d/coarse_grained/ligandr.pdb $RESULTS_DIR/$d/coarse_grained/receptorr.pdb $DISTANCE>$RESULTS_DIR/"$d"/$RESULTS/out-unbound.txt
        python $STEPS/all_coarse-grained_findandcut_script.py $RESULTS_DIR/$d/coarse_grained/ligandr-refe.pdb $RESULTS_DIR/$d/coarse_grained/receptorr-refe.pdb $DISTANCE $RESULTS_DIR/"$d"/$RESULTS/out-unbound.txt >$RESULTS_DIR/"$d"/$RESULTS/out-refe.txt
        mv $RESULTS_DIR/$d/coarse_grained/*bound-and-flexsep.pdb $RESULTS_DIR/$d/$RESULTS/
	
	
	###rest
	if ! [ -d $RESULTS_DIR/$d/$RESULTS/ligandr/ ]
        then
                mkdir -p $RESULTS_DIR/$d/$RESULTS/ligandr/
                python $STEPS/all_coarse-grained_adjusted-rest_script.py $RESULTS_DIR/$d/$RESULTS/ligandr_bound-and-flexsep.pdb >$RESULTS_DIR/$d/$RESULTS/rest_out-unbound.txt
                mv $RESULTS_DIR/$d/$RESULTS/ligandr_* $RESULTS_DIR/$d/$RESULTS/ligandr/
        fi

        if ! [ -d $RESULTS_DIR/$d/$RESULTS/ligandr-refe/ ]
        then

                mkdir -p $RESULTS_DIR/$d/$RESULTS/ligandr-refe/
                python $STEPS/all_coarse-grained_adjusted-rest_script.py $RESULTS_DIR/$d/$RESULTS/ligandr-refe_bound-and-flexsep.pdb >$RESULTS_DIR/$d/$RESULTS/rest_out-refe.txt
                mv $RESULTS_DIR/$d/$RESULTS/ligandr-refe_* $RESULTS_DIR/$d/$RESULTS/ligandr-refe/
        fi

	###attract
	bash $STEPS/doublechains.sh $d
        if [ -f $RESULTS_DIR/$d/$RESULTS/ligandr/ligandr_bound-and-flexsep.pdb ]
        then
                cd $RESULTS_DIR/$d/$RESULTS/ligandr/
                pdbfile=ligandr_bound-and-flexsep.pdb
                python $STEPS/all_attract-and-collect.py $pdbfile
                cd $INPUT_DIR
        fi

        if [ -f $RESULTS_DIR/$d/$RESULTS/ligandr-refe/ligandr-refe_bound-and-flexsep.pdb ]
        then
                cd $RESULTS_DIR/$d/$RESULTS/ligandr-refe/
                pdbfile=ligandr-refe_bound-and-flexsep.pdb
                python $STEPS/all_attract-and-collect.py $pdbfile
                cd $INPUT_DIR
        fi
        
    ###irmsd
        if [ -f $RESULTS_DIR/$d/$RESULTS/ligandr/ligandr_bound-and-flexsep_final.dat ]
        then
                cd $RESULTS_DIR/$d/$RESULTS/
                pdbfile=ligandr/ligandr_bound-and-flexsep.pdb
                refepdbfile=ligandr-refe/ligandr-refe_bound-and-flexsep.pdb
                python3 $STEPS/all_irmsd.py $pdbfile $refepdbfile
                cd $INPUT_DIR
        fi
    


done

