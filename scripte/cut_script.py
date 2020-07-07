#!/usr/bin/env python
# coding: utf-8

#import modules
import re 
import sys
import string
import os


#get input pdb file and output location as commandline argument
filename = sys.argv[1]
outputname = os.path.splitext(filename)[0]+'-separated.pdb'   
###print (filename)

#get cut postitions from user input
cut1= int(input("User input required, please type in!\nPosition of first flexible residue: ")) #use raw_input for python2
cut2= int(input("Position of last flexible residue: ")) #use raw_input for python2
#cut1 = sys.argv[3]
#cut2 = sys.argv[4]
###print cut1, cut2


#open pdb file 
###with open(filename, 'r') as pdb_file:
###  pdb = pdb_file.read()
###print (pdb)
for line in open(filename):
  pdblist = line.split() 
  #print(pdblist)

  #find classes
  position = int(pdblist[1])
  #residue = pdblist[3]
  residue_nr = int(pdblist[5])
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
    position = int(pdblist[1])
    #residue = pdblist[3]
    residue_nr = int(pdblist[5])
    
    if residue_nr < cut1_residue_nr :
      
      new_position+=1
      pdblist[1]= new_position
      pdblist[4]= alphabet_list[0]
      
      if residue_nr== cut1_residue_nr-1 and (pdblist[2]=="C" or pdblist[2]=="O"):
            pdblist[9]='99'
      print('\t'.join(map(str, pdblist)), file=output)

    elif residue_nr > cut2_residue_nr :
      new_position+=1
      pdblist[1]=new_position
      pdblist[4]=alphabet_list[0]
      
      if residue_nr== cut2_residue_nr+1 and pdblist[2]=="N":
        pdblist[9]='99'
      print('\t'.join(map(str, pdblist)), file=output)
        

#get cutted residues
#split in separated residues and add new chain labels  
  cutted_residue_nr=0
  chain_nr=0  
  for line in open(filename):
    pdblist = line.split()

    #find classes
    position = int(pdblist[1])
    residue = pdblist[3]
    residue_nr = int(pdblist[5])

    if (residue_nr >= cut1_residue_nr and residue_nr <= cut2_residue_nr):
      #add "TER" as residue separator
      #print(pdblist)
      if cutted_residue_nr==residue_nr:
        if pdblist[2]=='C' or pdblist[2]=='O':
            pdblist[9]='99'
      else:
        if pdblist[2]=="N":
            pdblist[9]='99'
        print("TER", file=output)
        chain_nr+=1
      #print(pdblist)
        #print(chain_nr)
      new_position+=1
      pdblist[1]=new_position
      pdblist[4]=alphabet_list[chain_nr]
      print('\t'.join(map(str, pdblist)), file=output)
      cutted_residue_nr=residue_nr

  print("TER", file=output)
  chain_nr+=1
  #print(chain_nr)

### add at beginning of the file a line defining the chain number of the pdb file
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(line)+ '\n' + content)
        
line_prepender('out.txt', chain_nr)
#adapting format with awk command



def awk_runner(inputfile, outputfile):
    cmd = r'''awk '/ATOM/{printf "%-4s%7d%1s%-5s%-4s%1s%4d%12.3f%8.3f%8.3f%2s%3d%8.3f%2d%5.2f \n", $1,$2," ",$3,$4,$5,$6,$7,$8,$9," ",$10,$11,$12,$13} !/ATOM/{print $1}' ''' + inputfile + " > " + outputfile
    os.system(cmd)


awk_runner('out.txt', outputname)
os.remove('out.txt')