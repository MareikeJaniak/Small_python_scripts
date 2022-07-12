#!/usr/bin/env python3

import sys
from glob import glob
from os import path

# read from input
sample = str(sys.argv[1])

script_dir = sys.path[0]
assembly_dir = path.dirname(path.abspath(script_dir))+"/assembly_out/"+sample

target = set(list(range(1, 3211)))

#find all filterd contigs for sample
filtered_files = glob(assembly_dir+"/*.filtered_contigs.fasta")

#strip redundant info from file names to create set of assembled contigs
filtered_files = [x.replace('.filtered_contigs.fasta', '') for x in filtered_files]
filtered_files = [x.replace(sample, '') for x in filtered_files]
filtered_files = [x.replace('_Node_', '') for x in filtered_files]
filtered_files = [x.replace('/scratch/mcj43/Salford/aTRAM/assembly_out//.', '') for x in filtered_files]

# turn list of stripped file names into set
present = list(map(int, filtered_files))
present = set(present)

# find missing loci by finding difference between target and present:
print(sorted(target.difference(present)))
