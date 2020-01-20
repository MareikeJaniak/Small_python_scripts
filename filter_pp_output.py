#!/usr/bin/env python3

import pandas as pd
import sys

PPfile = sys.argv[1]

# from PseudoPipe output filter calls that do not contain any insertions, deletions, shifts, or stops (0 in all of those columns)

PPGelada = pd.read_csv(PPfile, sep='\t', header=0)

PPGelada_filtered = PPGelada[(PPGelada.ins !=0) & (PPGelada.dels !=0) & (PPGelada.shift !=0) & (PPGelada.stop !=0)]

PPGelada_filtered.to_csv('/home/mcj43/scratch/Gelada_project/PseudoPipe/gelada/ppipe_output/gelada/pgenes/gelada_pgenes_filtered.txt', sep = '\t')
