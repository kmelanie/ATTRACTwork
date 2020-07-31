#!/usr/bin/env python
# coding: utf-8

#import modules
import re 
import sys
import string
import os
from Bio.PDB import PDBParser
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

#get input pdb file and output location as commandline argument
filename = 'receptor_ligand.txt'


###get input pdb file and output location as commandline argument and distance threashold for flexible amino acids 
ligand_name = sys.argv[1]
receptor_name=sys.argv[2]
distance_range=int(sys.argv[3])
outputname = os.path.splitext(ligand_name)[0]+'_bound-and-flexsep.pdb'
#print (filename)

# open outputfile 
### generate a file containing receptor and ligand with continuos Atom number and continuos residue number
atom_nr=1
with open('receptor_ligand.txt', 'w') as output: 
#get uncutted residues
  for line in open(receptor_name):
    pdblist = line.split()
    pdblist[1]=atom_nr
    print('\t'.join(map(str, pdblist)), file=output)
    atom_nr+=1
    residue_nr=pdblist[5]
  print('TER', file=output) 
  
  residue_offset=residue_nr
  offset=atom_nr-1
  print('Offset=', offset,'\nResidue Offset=',residue_offset)
  for line in open(ligand_name):
    pdblist = line.split()
    pdblist[1]=atom_nr
    pdblist[5]=str(int(residue_offset)+int(pdblist[5]))
    print('\t'.join(map(str, pdblist)), file=output)
    atom_nr+=1
    
# create parser to find distance between C-alpha atoms of ligand and all C-alpha atoms of receptor
parser = PDBParser()
alphabet_str= string.ascii_uppercase
alphabet_list=list(alphabet_str)

# read structure of ligand from file
structure = parser.get_structure('LIGAND',ligand_name)
model_ligand = structure[0]
for i in list(string.ascii_uppercase):
    try:
        chain_ligand = model_ligand[i]
    except KeyError:
        continue

# read structure of receptor from file
structure = parser.get_structure('RECEPTOR', receptor_name)
model_receptor = structure[0]
for i in list(string.ascii_uppercase):
    try:
        chain_receptor = model_receptor[i]
    except KeyError:
        continue



### find distance between residue of ligand and all residues of receptor
### two nested loops through all atoms of ligand and all atoms of receptor to find all residues within the given C-alpa distance threshold
close_residues=[]
for residue1 in chain_ligand:
    #print(residue1)
    for residue2 in chain_receptor:
        if residue1 != residue2:
            # compute distance between CA atoms
            try:
                distance = residue1['CA'] - residue2['CA']
            except KeyError:
                ## no CA atom, e.g. for H_NAG
                continue
            ### find residues with distance shorter than given threashold (here 7 Angstrom)
            if distance < distance_range:
                #print(residue1, residue2, distance)
                if residue1.get_full_id()[3][1] not in close_residues:
                    close_residues.append(residue1.get_full_id()[3][1])
                #print(residue1.get_full_id()[3][1])
#print(close_residues)

#exclude first amino acid of ligand to avoid including receptor amino acids due to addition of neighbouring amino acids in following steps... 
if close_residues[0] <= 1:
    del close_residues[0]

### get dictionary with flexible residues in loop clusters:
def grouper(iterable, threshold):
    prev = None
    group = []
    for item in iterable:
        if not prev or item - prev <= threshold:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group
flex_loops_dict=dict(enumerate(grouper(close_residues, 2), 1))
#print(flex_loops_dict)

### get first and last residue of loops as cut positions:
cut_pos=[]
for i in flex_loops_dict:
    if len(flex_loops_dict[i])>1:
        cut_pos.append([flex_loops_dict[i][0]-1,flex_loops_dict[i][-1]+1])
#print(cut_pos)

### get first and last residue of loops as cut positions:
cut_pos=[]
for i in flex_loops_dict:
    if len(flex_loops_dict[i])>1:
        cut_pos.append([flex_loops_dict[i][0]-1,flex_loops_dict[i][-1]+1])
        
chain_nr=1 

letters = list(string.ascii_uppercase)
num_cols = 200
alphabet_list=list(string.ascii_uppercase+string.ascii_lowercase+string.ascii_uppercase+string.ascii_lowercase)
del alphabet_list[52:54]
#alphabet_list = []
#for i in range(0, num_cols - 1):
#    n = i//26
#    m = n//26
#    i-=n*26
#    n-=m*26
#    col = letters[m-1]+letters[n-1]+letters[i] if m>0 else letters[n-1]+letters[i] if n>0 else letters[i]

### if ligand is already cutted, get flexible residues of ligand and use them as cut positions instead of the ones calculated in the lines above to enable comparasion of results
try: 
    ligand_out=sys.argv[4]
    cut_list=[]
    for line in open(ligand_out):
        cut_line = line.split()
        cut_list.append(cut_line)
    #print(cut_list)
    offset=int(cut_list[0][1])
    residue_offset=int(cut_list[1][2])
    print('Used values determined in the ligands run:\n****\nOffset=', offset,'\nResidue Offset=',residue_offset)
    cut_pos=[]
    for cut in cut_list[2:]:
        cut_pos.append([int(cut[0])-int(residue_offset), int(cut[1])-int(residue_offset)])
    #print(cut_pos)
   
except:
    pass
    
#get residue numbers of flexible amino acids and write to standart output (out-unbound.txt or out-bound.txt)   
for i in range(len(cut_pos)):
    cut1_residue_nr=cut_pos[i][0]+int(residue_offset)
    cut2_residue_nr=cut_pos[i][1]+int(residue_offset)
    edit=str(i)+'out.txt'
    if i==0:
        oldedit=filename
    else:
        oldedit=str(i-1)+'out.txt'
    print(cut1_residue_nr, cut2_residue_nr, edit)

    # get uncutted and cutted residues separated and write to output file 
    new_position=0 




    
    chain=alphabet_list[0]
    # open outputfile 
    with open(edit, 'w') as output: 
    #get uncutted residues
      for line in open(oldedit):
        pdblist = line.split()

        if pdblist[0]=='ATOM':
          #find classes
          position = int(pdblist[1])
          #residue = pdblist[3]
          residue_nr = int(pdblist[5])

          if residue_nr < cut1_residue_nr :

            new_position+=1
            pdblist[1]= new_position
            if i==0 and int(new_position)>offset:
                pdblist[4]=alphabet_list[1]
            elif i==0:
                pdblist[4]= alphabet_list[0]

            if residue_nr== cut1_residue_nr-1 and (pdblist[2]=="C" or pdblist[2]=="O"):
                pdblist[9]='99'
            print('\t'.join(map(str, pdblist)), file=output)

          elif residue_nr > cut2_residue_nr :
            new_position+=1
            pdblist[1]=new_position
            if i==0 and int(new_position)>offset:
                pdblist[4]=alphabet_list[1]
            elif i==0:
                pdblist[4]= alphabet_list[0]

            if residue_nr== cut2_residue_nr+1 and pdblist[2]=="N":
              pdblist[9]='99'
            print('\t'.join(map(str, pdblist)), file=output)
        else:
          print('\t'.join(map(str, pdblist)), file=output)


    #get cutted residues
    #split in separated residues and add new chain labels  
      cutted_residue_nr=0
 
      for line in open(oldedit):
        pdblist = line.split()
        if pdblist[0]=='ATOM':
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
      if i==len(cut_pos)-1:
          print("TER", file=output)
          chain_nr+=1
          #print(chain_nr)
      os.remove(oldedit)
        
### add at beginning of the file a line defining the chain number of the pdb file
def line_prepender(filetoprep, line):
    with open(filetoprep, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(line)+ '\n' + content)
        
line_prepender(edit, chain_nr)

#adapting format with awk command to receive output in correct PDB format
def awk_runner(inputfile, outputfile):
    cmd = r'''awk '/ATOM/{printf "%-4s%7d%1s%-5s%-4s%1s%4d%12.3f%8.3f%8.3f%2s%3d%8.3f%2d%5.2f \n", $1,$2," ",$3,$4,$5,$6,$7,$8,$9," ",$10,$11,$12,$13} !/ATOM/{print $1}' ''' + inputfile + " > " + outputfile
    os.system(cmd)


awk_runner(edit, outputname)
os.remove(edit)