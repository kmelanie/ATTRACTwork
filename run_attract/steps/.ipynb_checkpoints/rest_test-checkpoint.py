#!/usr/bin/env python
# coding: utf-8

###import modules
import re 
import sys
import string
import os
import ast

###get input pdb file and output location as commandline argument
filename = sys.argv[1]
#print (filename)



###define restraints
restraints={}
rest_dihedrals=ast.literal_eval(sys.argv[2])
rest_angles=ast.literal_eval(sys.argv[3])
rest_bond=ast.literal_eval(sys.argv[4])
restraints['rest_dihedrals']=rest_dihedrals
restraints['rest_angles']=rest_angles
restraints['rest_bond']=rest_bond
print(restraints)