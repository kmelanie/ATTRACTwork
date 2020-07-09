#!/bin/bash
d=$1 
if [ -d results/$d/cutted_distance10_new/ligandr/ ]
then
    cd results/$d/cutted_distance10_new/ligandr/
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
    cd ../../../../
fi
        
if [ -d results/$d/cutted_distance10_new/ligandr-refe/ ]
then
    cd results/$d/cutted_distance10_new/ligandr-refe/

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
    cd ../../../../
fi