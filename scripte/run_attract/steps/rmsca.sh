#!/bin/bash
##
# Melanie Käser
# T38 - July 2020
#
# Run ATTRACT (see https://github.com/glennclarence/attract)
# GitHub project: ATTRACTwork (see https://github.com/kmelanie/ATTRACTwork)
##

#
# Load the parameters
#

source /home/melaniekaser/attract-master/generat/work/scripte/run_attract/config_all-cut-rest-attract.sh



d=$1 
if [ -f $RESULTS_DIR/$d/$RESULTS/ligandr/ligandr*all.pdb ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr/
    grep -n 'MODEL\|ENDMDL' ligandr_bound-and-flexsep_all.pdb | cut -d: -f 1 |awk '{if(NR%2) printf "sed -n %d,",$1+1; else printf "%dp ligandr_bound-and-flexsep_all.pdb > model_%03d.pdb\n", $1-1,NR/2;}' |  bash -sf
    
    models=$(ls ./model*)
    for model in $models;
    do 
        $STEPS/rmsca ligandr_bound-and-flexsep.pdb $model >>intra-rmsca.dat 
    done  
    mkdir -p models
    for model in $models
    do
        mv $model models/    
    done
    cd $INPUT_DIR
fi
        
if [ -f $RESULTS_DIR/$d/$RESULTS/ligandr-refe/ligandr*all.pdb ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr-refe/
    grep -n 'MODEL\|ENDMDL' ligandr-refe_bound-and-flexsep_all.pdb | cut -d: -f 1 |awk '{if(NR%2) printf "sed -n %d,",$1+1; else printf "%dp ligandr-refe_bound-and-flexsep_all.pdb > model_%03d.pdb\n", $1-1,NR/2;}' |  bash -sf
    models=$(ls ./model*)
    for model in $models;
    do 
        $STEPS/rmsca ligandr-refe_bound-and-flexsep.pdb $model >>intra-refe-rmsca.dat 
    done  
    mkdir -p models
    for model in $models
    do
        mv $model models/    
    done
    cd $INPUT_DIR
fi

if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr/models/ ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr/
    models=$(ls ./models/model*)
    for model in $models;
    do 
        $STEPS/rmsca ../ligandr-refe/ligandr-refe_bound-and-flexsep.pdb $model >>inter-rmsca.dat 
    done  
    cd $INPUT_DIR
fi