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
if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr/ ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr/
    chains=$(ls *chain*)
    for chain in $chains;
    do 
        residues=$( awk '/ATOM/{print $6}' $chain | uniq )
        residue_count=1
        for i in $residues; 
        do
            awk '/'" $i "'/{if($6=='"$i"') print $0} END{print "TER"}' $chain > ${chain}$residue_count
            #echo $residue_count
            residue_count=$(($residue_count + 1))
        done
        if ! [ -f ${chain}2 ]
        then 
            library=$(ls ${chain}[0-9]*)
            for lib in $library
            do 
                rm $lib
            done
        fi
    done
    receptor=$(ls *A*[0-9]*)
    for chain in $receptor
    do 
         rm $chain
    done
    ligand=$(ls *B*[0-9]*)
    for chain in $ligand
    do
        rm $chain
    done
    for chain in $chains
    do 
        if [ -f ${chain}2 ]
        then
            mv ${chain} double${chain}
            mv ${chain}1 ${chain}
        fi
    done
    cd $INPUT_DIR
fi
        
if [ -d $RESULTS_DIR/$d/$RESULTS/ligandr-refe/ ]
then
    cd $RESULTS_DIR/$d/$RESULTS/ligandr-refe/

    chains=$(ls *chain*)
    for chain in $chains;
    do 
        residues=$( awk '/ATOM/{print $6}' $chain | uniq )
        residue_count=1
        for i in $residues; 
        do
            awk '/'" $i "'/{if($6=='"$i"') print $0} END{print "TER"}' $chain > ${chain}$residue_count
            #echo $residue_count
            residue_count=$(($residue_count + 1))
        done
        if ! [ -f ${chain}2 ]
        then 
            library=$(ls ${chain}[0-9]*)
            for lib in $library
            do 
                rm $lib
            done
        fi
    done
    receptor=$(ls *A*[0-9]*)
    for chain in $receptor
    do 
        rm $chain
    done
    ligand=$(ls *B*[0-9]*)
    for chain in $ligand
    do
        rm $chain
    done
    for chain in $chains
    do 
        if [ -f ${chain}2 ]
        then
            mv ${chain} double${chain}
            mv ${chain}1 ${chain}
        fi
    done
    cd $INPUT_DIR
fi