#!/usr/bin/env python3

# find genes that are annotated as pseudogenes by both PseudoPipe and SnpEff output. PseudoPipe annotated with gelada ensembl protein ID, SnpEff annotated with baboon entrezgene accession.

import pandas as pd
import numpy as np

pp_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/ppipe_output/gelada/pgenes/gelada_pgenes_filtered.txt', sep='\t')
ID_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/matched_IDs.tsv', sep='\t')
SnpEff_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/SnpEff/filteredVCF/geladas.panu3.snpEff.filtered.HIGH.STOPGAINED.NO-NON-ALT.recode.annotate.EXTRACT.vcf',sep='\t')

pp_df["query"] = pp_df["query"].str.replace('\.1','')

overlap = np.intersect1d(pp_df["query"], ID_df["Protein_ID_Tgel"])

matched_IDs_pp = ID_df[ID_df.Protein_ID_Tgel.isin(overlap)]

#overlap_pp_SnpEff = np.intersect1d(matched_IDs_pp["GeneSymbol"], SnpEff_df["GENE"])
#print(overlap_pp_SnpEff)
out = matched_IDs_pp[matched_IDs_pp["NCBI_gene_Panu"].isin(SnpEff_df["GENE"])]

with open("/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/Pseudogenes_overlap_PP_SnpEff.tsv", "w") as outfile:
	out.to_csv(outfile, sep='\t', index=False)
