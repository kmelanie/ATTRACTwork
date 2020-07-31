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

pdblist_list=[]
for line in open(filename):
    pdblist = line.split() 
    ###print pdblist
    pdblist_list.append(pdblist)

#print(pdblist_list)

###get cut positions by separator "TER"
cut_positions=[]
cut_positions=[i for i, n in enumerate(pdblist_list) if n == ["TER"]]
del cut_positions[0]
cut_positions.insert(0,0)
#print(cut_positions)

###create dictionary with chainlists as value and chain label letter as key 
residue_dict={}
chain_label_list=[]
for cut in cut_positions:
    index=cut_positions.index(cut)
    #print(index)
    residue=pdblist_list[cut_positions[index-1]:cut]
    #print(pdblist_list[cut+1])
    if cut!=cut_positions[-1]:
        chain_label=pdblist_list[cut+1][4]
        #print(chain_label)
        chain_label_list.append(chain_label)
    if index>0:
        residue_dict[chain_label_list[index-1]]=residue
        #print(residue_dict)

#print(residue_dict["A"])
#print(residue_dict["C"])
#print(chain_label_list)

###create dictionary with chainlists as value LR as key for the last rigid aminoacid and FR as key for the first rigid aminoacid

### get last rigid residue as user input
#cut1= input("User input required, please type in!\nPosition of last rigid residue: ") #use raw_input for python2
flex_resnumbers=[]
for pdblist in pdblist_list:
    for cut in cut_positions[1:]:
        #print(pdblist)
        index=pdblist_list.index(pdblist)
        if len(pdblist)==13 and index==cut+1:
            res=int(pdblist[5])-1
            flex_resnumbers.append(res)
LR_resnumbers=flex_resnumbers.copy()
for res in flex_resnumbers[1:]:
    index=flex_resnumbers.index(res)
    if res==flex_resnumbers[index-1]+1:
        LR_resnumbers.remove(res)
#print(LR_resnumbers)
#print(flex_resnumbers)

### get last rigid residue using residue number (pdblist[5]) of first flexible amino acid 
#for pdblist in pdblist_list:
    #print(pdblist)
#    if len(pdblist)==13 and int(pdblist[1])==cut_positions[1]+1:
#        cut1_res=int(pdblist[5])-1
#for pdblist in pdblist_list:
    #print(pdblist[1])
##    if len(pdblist)==13 and int(pdblist[5])==cut1_res:
#        cut1=int(pdblist[1])-1
#print(cut1_res)
#print(str(cut1)+ " - position of C in last rigid residue")
#print(str(cut1+2)+ " - position of N in first rigid residue")

 
rigid_dict={}


###find all Atoms in pdblist for last rigid aminoacid (LR) befor cut position 
#rigid_dict['LR']=[["TER"]]
#for pdblist in pdblist_list:
#    if len(pdblist)>1 and pdblist[1]==str(cut1):
        #print(pdblist[1])
#        LR_residue_nr=pdblist[5]
for LR in LR_resnumbers:
    rigid_dict['LR'+str(LR)]=[["TER"]]
for pdblist in pdblist_list:
    #print(pdblist)
    for LR in LR_resnumbers:
        #print(type(LR))
        if len(pdblist)>1 and int(pdblist[5])==LR:
            rigid_dict['LR'+str(LR)].append(pdblist)
#print(rigid_dict)

FR_resnumbers=[]
for pdblist in pdblist_list:
    for LR in LR_resnumbers:
        if len(pdblist)>1 and pdblist[1]==str(int(rigid_dict['LR'+str(LR)][-1][1])+1):
            FR_resnumbers.append(pdblist[5])
#print(FR_resnumbers)

for FR in FR_resnumbers:
    rigid_dict['FR'+str(FR)]=[["TER"]]
for pdblist in pdblist_list:
    #print(pdblist)
    for FR in FR_resnumbers:
        if len(pdblist)>1 and pdblist[5]==FR:
            rigid_dict['FR'+str(FR)].append(pdblist)
#print(rigid_dict)


### fuse dictonary containing all residues (residue_dict) with dictonary defining the last and first rigid residue (rigid_dict)
extended_residue_dict=residue_dict.copy()
extended_residue_dict.update(rigid_dict)
#print(extended_residue_dict)


### define order of residues in chain lable list
#print(chain_label_list)
sort_dict={}
for entry in extended_residue_dict:
    sort_dict[entry]=extended_residue_dict[entry][1][5]
#print(sort_dict)

extended_chain_label_list=[]
sort_list=sorted(sort_dict.items(), key = 
             lambda kv:(kv[1], kv[0]))
for res in sort_list:
    extended_chain_label_list.append(sort_list[sort_list.index(res)][0])
#prin-t(extended_chain_label_list)

###get atom positions of bonds, angles and dihedrals

N={}
C={}
CA={}
O={}
#HN={}
for aa in extended_chain_label_list[1:]:
    #N[aa]=extended_residue_dict[aa][1][1]
    #C[aa]=extended_residue_dict[aa][-2][1]
    
    for atom in extended_residue_dict[aa][1:]:
        if atom[2]=="CA":
            CA[aa]=atom[1]
        elif atom[2]=="C":
            C[aa]=atom[1]
        elif atom[2]=="O":
            O[aa]=atom[1]
        elif atom[2]=="N":
            N[aa]=atom[1]
    #O[aa]=extended_residue_dict[aa][-1][1]
#    if extended_residue_dict[aa][2][2]=="HN":
#        HN[aa]=extended_residue_dict[aa][2][1]
#        ### Exeption: amino acid proline does not have an atom HN --> choose delta C (CD) instead for atom3 in angle4
#      else:
#        if extended_residue_dict[aa][5][2]=="CD":
#            HN[aa]=extended_residue_dict[aa][5][1]
#print(O,N,C,CA)

###create dictionary with chain lable letter as key and dihedrals of peptide bond as value
dihedrals={}
for aa in (aa for aa in extended_chain_label_list[2:] if not aa.startswith('LR')):
    #print(aa)
    index=extended_chain_label_list.index(aa)
    ###define four backbone dihedrals per peptide bond
    dihedral1=['4',CA[extended_chain_label_list[index-1]],C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]],CA[extended_chain_label_list[index]]]
    dihedral2=['4',O[extended_chain_label_list[index-1]],C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]],CA[extended_chain_label_list[index]]]
    dihedral3=['4',N[extended_chain_label_list[index-1]],CA[extended_chain_label_list[index-1]],C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]]]
    dihedral4=['4',C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]],CA[extended_chain_label_list[index]],C[extended_chain_label_list[index]]]
    
    dihedrals[aa]=dihedral1, dihedral2, dihedral3, dihedral4
    
#print(dihedrals)

###create dictionary with chain lable letter as key and angles of peptide bond as value
angles={}
for aa in (aa for aa in extended_chain_label_list[2:] if not aa.startswith('LR')):
    index=extended_chain_label_list.index(aa)
    ###define four backbone angles per peptide bond
    angle1=['3',CA[extended_chain_label_list[index-1]],C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]]]
    angle2=['3',O[extended_chain_label_list[index-1]],C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]]]
    angle3=['3',C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]],CA[extended_chain_label_list[index]]]
### angle 4 can not be adjusted in coarse grained models because position of HN is missing.
    #    angle4=['3',C[extended_chain_label_list[index-1]],N[extended_chain_label_list[index]],HN[extended_chain_label_list[index]]]
    
    angles[aa]=angle1, angle2, angle3 #,angle4
    
#print(angles)

bond={}
for aa in (aa for aa in extended_chain_label_list[2:] if not aa.startswith('LR')):
    index=extended_chain_label_list.index(aa)
    ###define two atoms per peptide bond
    atom1=['1',C[extended_chain_label_list[index-1]]]
    atom2=['1',N[extended_chain_label_list[index]]]
    
    bond[aa]=atom1,atom2
    
#print(bond)

### create lable list for output
lable_list= ["a"+str(i) for i in range((len(extended_chain_label_list)-2)*10)]
#print(list_test)

###generate output in right format
lable=0
rest_file=os.path.splitext(filename)[0]+'_adjusted.rest'   
with open(rest_file, 'w') as output: 
    for aa in (aa for aa in extended_chain_label_list[2:] if not aa.startswith('LR')):
        for dihedral in dihedrals[aa]:
            dihedral.insert(0,lable_list[lable])
            print(' '.join(dihedral), file=output)
            lable+=1
        for angle in angles[aa]:
            angle.insert(0,lable_list[lable])
            print(' '.join(angle), file=output)
            lable+=1
        for atom in bond[aa]:
            atom.insert(0,lable_list[lable])
            print(' '.join(atom), file=output)
            lable+=1
            
            
###generate second block of output .rest file with restraints of angles, dihedrals and bonds

###get restraints from command line argument passed by variables defined in the config file
    restraints={}
    rest_dihedrals=ast.literal_eval(sys.argv[2])
    rest_angles=ast.literal_eval(sys.argv[3])
    rest_bond=ast.literal_eval(sys.argv[4])
    restraints['rest_dihedrals']=rest_dihedrals
    restraints['rest_angles']=rest_angles
    restraints['rest_bond']=rest_bond
###define restraints hard coded if restraints are not yet defined in config file and passed by command line arguments
    #restraints={}
    #rest_dihedrals=[[3.1415,60.1],[0,60.1],[1.0,0.51],[-2.4,2.1]]
    #restraints['rest_dihedrals']=rest_dihedrals
    #restraints['rest_angles']=[[2.02,55.1],[2.13,55.1],[2.13,55.1],[2.09,55.1]]
    #restraints['rest_bond']=[[1.35,300.1]]
    #print(restraints)
    
    print(" ", file=output)
    for aa in (aa for aa in extended_chain_label_list[2:] if not aa.startswith('LR')):
        for dihedral in dihedrals[aa]:
            index=dihedrals[aa].index(dihedral)
            print(dihedral[0],dihedral[0],"10",restraints['rest_dihedrals'][index][0],restraints['rest_dihedrals'][index][1], file=output)
        for angle in angles[aa]:
            index=angles[aa].index(angle)
            print(angle[0],angle[0],"9",restraints['rest_angles'][index][0],restraints['rest_angles'][index][1], file=output)            
            #print(angle[0],angle[0],"9", file=output)
        print(bond[aa][0][0],bond[aa][1][0],"4",restraints['rest_bond'][0][0],restraints['rest_bond'][0][1], file=output)


### generate start file in .dat format
chain_label_list.insert(1,"B")
#print(chain_label_list)
#start_dat={}
#for chain in chain_label_list[:]:
#    print(chain)
#    start_dat[chain]=[0,0,0,0,0,0]
start_dat_file=os.path.splitext(filename)[0]+'-start.dat'   
with open(start_dat_file, 'w') as output:
    print('#pivot auto\n#centered receptor: false\n#centered ligands: false\n#1', file=output)
    for chain in chain_label_list[:]:
        print(' '.join(map(str, [0,0,0,0,0,0])), file=output)

### generate single chain pdb files

def awk_runner(inputfile, outputfile):
    cmd = r'''awk '/ATOM/{printf "%-4s%7d%1s%-5s%-4s%1s%4d%12.3f%8.3f%8.3f%2s%3d%8.3f%2d%5.2f \n", $1,$2," ",$3,$4,$5,$6,$7,$8,$9," ",$10,$11,$12,$13} !/ATOM/{print $1}' ''' + inputfile + " > " + outputfile
    os.system(cmd)

for chain in chain_label_list[:]:
    file=os.path.splitext(filename)[0]
    chain_file=chain+'.pdb'
    chain_file2=file+'-chain'+chain+'.pdb'
    with open(chain_file,'w') as output:
        for pdblist in pdblist_list:
            if pdblist[0]=="ATOM" and pdblist[4]==chain:
                print('\t'.join(map(str, pdblist)), file=output)
        print('TER', file=output)
    awk_runner(chain_file, chain_file2)
    os.remove(chain_file)
