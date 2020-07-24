#!/usr/bin/env python
# coding: utf-8

import os
import sys
from string import ascii_uppercase
from string import ascii_lowercase

pdbfile=str(sys.argv[1])
file=os.path.splitext(pdbfile)[0]

letters = list(ascii_uppercase+ascii_lowercase+ascii_uppercase+ascii_lowercase)
del letters[52:54]

#print("Current Working Directory " , os.getcwd())



for line in open(pdbfile):
    pdblist=line.split()
    endchain=pdblist[0]
    break
    
intra_irmsd=['python2 $ATTRACTDIR/irmsd.py '+file+'_final.dat']
chain_count=0
for i in letters[:int(endchain)]:
    chain_count+=1
    if chain_count<=52:
        intra_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb')
        intra_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb')
    if chain_count>52:
        intra_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
        intra_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
intra_irmsd=' '.join(map(str, intra_irmsd))+' > '+file+'_intra-irmsd.dat'
#print(intra-irmsd)
os.system(intra_irmsd)

intra_refe_irmsd=['python2 $ATTRACTDIR/irmsd.py '+file+'_final.dat']
chain_count=0
for i in letters[:int(endchain)]:
    chain_count+=1
    if chain_count<=52:
        intra_refe_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb')
        intra_refe_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb')
    if chain_count>52:
        intra_refe_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
        intra_refe_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
intra_refe_irmsd=' '.join(map(str, intra_refe_irmsd))+' > '+file+'_intra-refe-irmsd.dat'
#print(intra_refe_irmsd)
os.system(intra_refe_irmsd)


inter_irmsd=['python2 $ATTRACTDIR/irmsd.py '+file+'_final.dat']
chain_count=0
for i in letters[:int(endchain)]:
    chain_count+=1
    if chain_count<=52:
        inter_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb')
        inter_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb')
    if chain_count>52:
        inter_irmsd.append('./ligandr/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
        inter_irmsd.append('./ligandr-refe/ligand*_bound-and-flexsep-chain'+i+'.pdb2')
inter_irmsd=' '.join(map(str, inter_irmsd))+' > '+file+'_inter-irmsd.dat'
#print(inter_irmsd)
os.system(inter_irmsd)
