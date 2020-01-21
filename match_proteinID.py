#!/usr/bin/env python3

### script to extract ensembl protein id, gene id, and gene symbol from fasta header in protein sequence fasta file and write to tsv that contains three columns. In second step, matching entrezgene accessions from the Papio anubis genome (Panu_3.0) are added as a fourth column. 
# output used to find overlap between PseudoPipe and SnpEff results, which are annotated with different genomes.

import pandas as pd

lst = []

with open('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/ppipe_input/pep/Theropithecus_gelada.Tgel_1.0.pep.all.fa') as file:
	for line in file:
		if line.startswith('>'):
			line = line.rstrip()
			line = line.replace('>','')
			line = line.replace('gene:','')
			line = line.replace('.1','')
			if 'gene_symbol' in line:				# not all lines contain gene symbol info, leading to index out of range error
				line = line.replace('gene_symbol:','')
				line_list = line.split(' ')
				info_list = [str(line_list[0])]
				info_list.append(str(line_list[3]))
				info_list.append(str(line_list[7]))
				lst.append(info_list)
			else:							# solved by only extracting 7th index for lines that contain gene_symbol
				line_list = line.split(' ')
				info_list = [str(line_list[0])]
				info_list.append(str(line_list[3]))
				lst.append(info_list)
		else:
			continue

df = pd.DataFrame(lst, columns = ['Protein_ID_Tgel','GeneID','GeneSymbol'])

# add matched baboon entrezgene_accession to the df containing gelada proteinID, geneID, and geneSymbol (compiled with biomaRt)

df_PanuTgel = pd.read_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/matched_baboonEntrez_geladaEnsembl.tsv', sep='\t')

df_matched = pd.merge(df,df_PanuTgel, on='Protein_ID_Tgel', how='left')

#print(df_matched)
with open('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/matched_IDs.tsv', 'w') as out_file:
	df_matched.to_csv(out_file, sep='\t', index=False)
