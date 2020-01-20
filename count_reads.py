#!/usr/bin/env python3

import sys
import gzip

# count the number of reads in a fastq file

file = sys.argv[1]

reads = 0

with gzip.open(file, 'rb') as fastq:
	for id in fastq:
		read = next(fastq)
		reads += 1
		next(fastq)
		next(fastq)

print(file,'has',reads,'reads')
