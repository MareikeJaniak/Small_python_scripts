#!/usr/bin/env python3

# script to only keep lines with exon start and stop locations from gelada gff3 files. Name of chromosome is passed on command line.
# used to prep input files for PseudoPipe

import sys

chr = sys.argv[1]
file_name = "Theropithecus_gelada.Tgel_1.0.98.primary_assembly."+chr+".gff3"
outfile_name = "Chr"+chr+"_exon_loc.txt"

with open(file_name, 'r') as gff:
	with open(outfile_name, 'a') as exon_file:
		for line in gff:
			if "exon" in line:
				line = line.replace('ensembl\t', '')
				exon_file.write(line)
			else:
				continue
