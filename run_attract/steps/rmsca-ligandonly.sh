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
if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr/models ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr/models    
    models=$(ls ./model*)
    mkdir -p ligandonly
    for model in $models;
    do 
        awk '{if($5!="A") print $0}' $model > ligandonly/$model
        awk '{if($5!="A") print $0}' ../ligandr_bound-and-flexsep.pdb > ligandonly/ligandr_bound-and-flexsep_ligonly.pdb
        $STEPS/rmsca ligandonly/ligandr_bound-and-flexsep_ligonly.pdb ligandonly/$model >>../ligandonly_intra-rmsca.dat
    done  
    cd $INPUT_DIR
fi
        
if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr-refe/models ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr-refe/models
    models=$(ls ./model*)
    mkdir -p ligandonly
    for model in $models;
    do 
        awk '{if($5!="A") print $0}' $model > ligandonly/$model
        awk '{if($5!="A") print $0}' ../ligandr-refe_bound-and-flexsep.pdb > ligandonly/ligandr-refe_bound-and-flexsep_ligonly.pdb
        $STEPS/rmsca ligandonly/ligandr-refe_bound-and-flexsep_ligonly.pdb ligandonly/$model >>../ligandonly_intra-refe-rmsca.dat 
    done  
    cd $INPUT_DIR
fi

if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr/models/ ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr/models
    models=$(ls ./model*)
    for model in $models;
    do 
        $STEPS/rmsca ../../ligandr-refe/models/ligandonly/ligandr-refe_bound-and-flexsep_ligonly.pdb ligandonly/$model >>../ligandonly_inter-rmsca.dat 
    done  
    cd $INPUT_DIR
fi