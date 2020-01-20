#!/usr/bin/env python3

### script to extract ensembl protein id, gene id, and gene symbol from fasta header in protein sequence fasta file and write to tsv that contains three columns.

import pandas as pd

lst = []

with open('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/ppipe_input/pep/Theropithecus_gelada.Tgel_1.0.pep.all.fa') as file:
	for line in file:
		if line.startswith('>'):
			line = line.rstrip()
			line = line.replace('>','')
			line = line.replace('gene:','')
			if 'gene_symbol' in line:				# not all lines contain gene symbol info, leading to index out of range error
				line = line.replace('gene_symbol:','')
				line_list = line.split(' ')
				info_list = [str(line_list[0])]
				info_list.append(str(line_list[3]))
				info_list.append(str(line_list[7]))
				lst.append(info_list)
			else:							# solved by only extracting 7th index for lines that contain gene_symbol
				line = line.split(' ')
				info_list = [str(line_list[0])]
				info_list.append(str(line_list[3]))
				lst.append(info_list)

df = pd.DataFrame(lst, columns = ['ProteinID','GeneID','GeneSymbol'])

with open('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/matched_IDs.tsv', 'w') as out_file:
	df.to_csv(out_file, sep='\t', index=False)
