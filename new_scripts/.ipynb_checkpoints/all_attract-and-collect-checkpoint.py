#!/usr/bin/env python
# coding: utf-8

import os
import sys
from string import ascii_uppercase
from string import ascii_lowercase

pdbfile=str(sys.argv[1])
file=os.path.splitext(pdbfile)[0]

letters = list(ascii_uppercase+ascii_lowercase+ascii_uppercase)
del letters[52:54]

#print("Current Working Directory " , os.getcwd())

attract='$ATTRACTDIR/attract ./*start.dat $ATTRACTDIR/../attract.par  *bound-and-flexsep.pdb --rest ./*.rest --traj --vmax 100 > '+file+'final.dat'

for line in open(pdbfile):
    pdblist=line.split()
    endchain=pdblist[0]
    break
collect=['$ATTRACTDIR/collect '+file+'final.dat']
chain_count=0
for i in letters[:int(endchain)]:
    chain_count+=1
    if chain_count<=52:
        collect.append('./ligand*_bound-and-flexsep-chain'+i+'.pdb')
    if chain_count>52:
        collect.append('./ligand*_bound-and-flexsep-chain'+i+'.pdb2')
collect
collect=' '.join(map(str, collect))+' > '+file+'_all.pdb'
#print(collect)

os.system(attract)
os.system(collect)