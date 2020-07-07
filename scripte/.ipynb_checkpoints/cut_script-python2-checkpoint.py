#!/usr/bin/env python
# coding: utf-8

#import modules
import re 
import sys
import string
import os


#get input pdb file and output location as commandline argument
filename = sys.argv[1]
outputname = sys.argv[2]
###print (filename)

#get cut postitions from user input
cut1= raw_input("User input required, please type in!\nPosition of first flexible residue: ")
cut2= raw_input("Position of last flexible residue: ")
#cut1 = sys.argv[3]
#cut2 = sys.argv[4]
###print cut1, cut2


#open pdb file 
###with open(filename, 'r') as pdb_file:
###  pdb = pdb_file.read()
###print (pdb)
for line in open(filename):
  pdblist = line.split() 
  ###print pdblist


  #find classes
  position = pdblist[1]
  #residue = pdblist[3]
  residue_nr = pdblist[5]
  ###print position, residue, residue_nr
  
  #get residue_nr of cut positions
  if position == cut1 :
    cut1_residue_nr = residue_nr
  if position == cut2 :
    cut2_residue_nr = residue_nr

###print cut1_residue_nr, cut2_residue_nr

# get uncutted and cutted residues separated and write to output file 
new_position=0 
alphabet_str= string.ascii_uppercase
alphabet_list=list(alphabet_str)
chain=alphabet_list[0]
# open outputfile 
with open('out.txt', 'w') as output: 
#get uncutted residues
  for line in open(filename):
    pdblist = line.split()

    #find classes
    position = pdblist[1]
    #residue = pdblist[3]
    residue_nr = pdblist[5]
    
    if residue_nr < cut1_residue_nr :
      new_position+=1
      pdblist[1]= new_position
      pdblist[4]= alphabet_list[0]
      print >>output, '\t'.join(map(str, pdblist))

    elif residue_nr > cut2_residue_nr :
      new_position+=1
      pdblist[1]=new_position
      pdblist[4]=alphabet_list[0]
      print >>output, '\t'.join(map(str, pdblist))

#get cutted residues
#split in separated residues and add new chain labels  
  cutted_residue_nr=0
  chain_nr=0  
  for line in open(filename):
    pdblist = line.split()

    #find classes
    position = pdblist[1]
    residue = pdblist[3]
    residue_nr = pdblist[5]

    if residue_nr >= cut1_residue_nr and residue_nr <= cut2_residue_nr:
      #add "TER" as residue separator
      if cutted_residue_nr==residue_nr:
        pass
      else:
        print >>output,"TER"
        chain_nr+=1
      new_position+=1
      pdblist[1]=new_position
      pdblist[4]=alphabet_list[chain_nr]
      print >>output, '\t'.join(map(str, pdblist))
      cutted_residue_nr=residue_nr

  print >>output, "TER"


#adapting format with awk command

def awk_runner(inputfile, outputfile):
    cmd = r'''awk '/ATOM/{printf "%-4s%7d%2s%-4s%-4s%1s%4d%12.3f%8.3f%8.3f%2s%3d%8.3f%2d%5.2f \n", $1,$2," ",$3,$4,$5,$6,$7,$8,$9," ",$10,$11,$12,$13} /TER/{print $1}' ''' + inputfile + " > " + outputfile
    os.system(cmd)


awk_runner('out.txt', outputname)