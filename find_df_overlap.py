#!/usr/bin/env python3

import pandas as pd
import numpy as np

pp_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/ppipe_output/gelada/pgenes/gelada_pgenes_filtered.txt', sep='\t')
ID_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/matched_IDs.tsv', sep='\t')
SnpEff_df = pd.read_csv('/home/mcj43/scratch/Gelada_project/SnpEff/filteredVCF/geladas.panu3.snpEff.filtered.HIGH.STOPGAINED.NO-NON-ALT.recode.annotate.EXTRACT.vcf',sep='\t')

overlap = np.intersect1d(pp_df["query"], ID_df["ProteinID"])

matched_IDs_pp = ID_df[ID_df.ProteinID.isin(overlap)]

#overlap_pp_SnpEff = np.intersect1d(matched_IDs_pp["GeneSymbol"], SnpEff_df["GENE"])
#print(overlap_pp_SnpEff)
out = matched_IDs_pp[matched_IDs_pp["GeneSymbol"].isin(SnpEff_df["GENE"])]

with open("/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/overlap_pp_SnpEff.tsv", "w") as outfile:
	out.to_csv(outfile, sep='\t', index=False)
