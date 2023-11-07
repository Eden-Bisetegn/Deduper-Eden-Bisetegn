#!/usr/bin/env python

import argparse
import gzip
import re

def get_args():
    parser = argparse.ArgumentParser(description="This script can be used to remove duplicate reads from a given sorted sam file inconsideration of 5 prime soft clipping")
    parser.add_argument("-f", "--name", help="input file name", required=True)
    parser.add_argument("-o", "--output", help="output_filename", required=True)
    parser.add_argument("-u", "--UMI", help="UMI file", required=True)
    #parser.add_argument("-h", "--help", help="This script can be used to remove duplicate reads from a given sorted sam file inconsideration of 5 prime soft clipping ",)
    return parser.parse_args()

args=get_args()
filename= args.name
output=args.output
UMI=args.UMI

known_umi=[]  #list for known umi
uniqe_reads={} #dictionary for unique reads /key-value_tup value-not set
curr_chrom= None #helps to empty out the dictionary after a change in chromosome number
duplicate_count=0 # counter for duplicate reads 

#functions
# adjusting  position for sequences with soft clipping # cheaking cigar string
#rname = line[3]
#umi = line[1]
#pos = line[4]
#flag = int(line[2])
#cigar = line[6]

def adjust_position(cigar, pos, strand):
    '''Adjusts the posion of each read incase of 5 prime soft clipping inconsideration of forward and reverse strands.'''
    new_pos=0
    cigar=re.findall(r'(\d+)([MIDNS])', cigar)
    #print(cigar)
    if strand == "forward":
        if "S" in cigar[0][1]:
            new_pos=int(pos)-int(cigar[0][0])
            #print("adjusted position to", new_pos)
            return new_pos
        else:
            return pos
    elif strand == "reverse": 
        first_group =True
        for i, group in cigar: #loops through list of matches and adds them to the position 
            #print(f'{i} : {group}')
            if first_group and cigar[0][1] =='S':
                first_group=False
                continue
            if group =="M" or group == "D" or group =="N" or group =="S":
                new_pos+=int(i) #adds to the position number 
        adj_pos = new_pos + int(pos)
        #(f'newposition: {adj_pos}\n')
        return adj_pos

#print(f'Function check: {adjust_position("24S71M2S", 76814308, "reverse")}')

with open(UMI) as file:  # open umi file and put in a list
    for line in file:
        known_umi.append(line.strip())
#print(known_umi)
unknown_umi=0
record=0
with open (filename, 'r') as fh, open (output,'w') as out: # open input/output sam file  
    while True:
        line = fh.readline().strip() # split line so they can be referred by position

        if line == "": # if line is empty break while true loop
            # EOF 
            break
        
        if line.startswith('@'): # for the first lines - if it starts with @ put in file
            out.write(f'{line}\n')
            continue

        sam_line = line.split()

        rname = sam_line[2] #chrom  # name each position to make it easier to refer to
        qname = sam_line[0]   #umi
        pos = int(sam_line[3])   #
        flag = int(sam_line[1])
        cigar = sam_line[5]
        #print(umi)
        #if((flag & 4) == 4):  #cheaks if read is unmapped 
          #  continue

        if rname != curr_chrom:
            curr_chrom=rname
            uniqe_reads.clear()
        umi = qname.split(':')[7]
        umi = umi.split()[0]

        if umi not in known_umi: #cheaks if its in the list of known UMI's
            unknown_umi+=1
            continue
        else:
            umi=umi

            if((flag & 16) == 16): # if its the reverse complement / if it = TRUE strand is -ve / if FALSE strand is +ve
                strand='reverse'
            else:
                strand='forward'

            adj_pos=adjust_position(cigar,pos,strand)
            #print(f'Adjusted: {adj_pos}')
           
            #print(f'{umi} : {strand}')
            value_tup=(umi,strand,adj_pos)
            print(value_tup, end="\t")

            if value_tup in uniqe_reads: 
                uniqe_reads[value_tup] += 1
                duplicate_count+=1
                #print("A DUP")

            else:
                out.write(f'{line}\n')
                uniqe_reads[value_tup] = 1
                record+=1
                #print("UNIQ")

with open('summary.txt', 'w') as summary:   
    summary.write(f'duplicate: {duplicate_count}\nNumber of reads: {record}\nUnknown UMIs: {unknown_umi}\n')