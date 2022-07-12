#!/bin/env python3

import pandas as pd
from glob import glob
import os
from os import path
import sys

# Set cwd to script location
script_dir = sys.path[0]

# Identify output directory
output_dir = path.dirname(path.abspath(script_dir))+"/output"
mito_dir = path.dirname(path.abspath(script_dir))

# Initialize pandas df to get number of contigs found per sample, length of final contig, and number of genes annotated
df = pd.DataFrame(columns=['Sample','ContigsFound','LengthFinalContig','GenesAnnotated'])
df2 = pd.DataFrame(columns=['Sample','ContigsFound','ContigNum','ContigLength','ContigCov'])

# List all samples based on log files present
files = sorted(glob(output_dir+"/*_MitoFinder.log"))
samples = [x.replace('_MitoFinder.log', '') for x in files]
samples = [x.replace(output_dir+'/', '') for x in samples]

for sample in samples:
	out = list()
	out.append(sample)
	
	# get number of contigs found from log file
	with open(output_dir+'/'+sample+'_MitoFinder.log', 'r') as file:
		lines = file.readlines()
		for line in lines:
			if "MitoFinder found" in line:
				if "a single" in line:
					contigs = "1"
					out.append(contigs)
				else:
					x = line.split()
					contigs = x[2]
					out.append(contigs)
			elif "MetaSPAdes didn't run well" in line:
				contigs = "NA"
				out.append(contigs)

	# get length of final contig from files
	if contigs == "1":
		with open(output_dir+'/'+sample+'/'+sample+'_MitoFinder_metaspades_mitfi_Final_Results/'+sample+'.infos', 'r') as file:
			lines = file.readlines()
			for line in lines:
				if "Length:" in line:
					x = line.split()
					length = x[1]
					out.append(length)
	elif contigs == "NA":
		length = "NA"
		out.append(length)
	else:
		with open(output_dir+'/'+sample+'/'+sample+'_MitoFinder_metaspades_mitfi_Final_Results/'+sample+'_mtDNA_contig_1.infos', 'r') as file:
			lines = file.readlines()
			for line in lines:
				if "Length:" in line:
					x = line.split()
					length = x[1]
					out.append(length)

	# get number of genes annotated in final contig from log files
	if contigs == "1":
		with open(output_dir+'/'+sample+'_MitoFinder.log', 'r') as file:
			lines = file.readlines()
			for line in lines:
				if "genes were found in mtDNA_contig" in line:
					x = line.split()
					genes = x[0]
					out.append(genes)
	elif contigs == "NA":
		genes = "NA"
		out.append(genes)
	else:
		with open(output_dir+'/'+sample+'/geneChecker.log', 'r') as file:
			lines = file.readlines()
			for line in lines:
				if "Features found:" in line:
					x = line.split()
					genes = x[2]
					out.append(genes)
		# for samples with multiple contigs also get length and coverage for each contig and save to separate df
		sampleNameList = list()
		contigNumberList = list()
		contigNameList = list()
		contigLengthList = list()
		contigCovList = list()

		contig_files = sorted(glob(output_dir+"/"+sample+"/"+sample+"_contig_*.fasta"))
		contig_names = [x.replace(output_dir+'/'+sample+'/'+sample+'_', '') for x in contig_files]
		contig_names = [x.replace('.fasta', '') for x in contig_names]
		for contig in contig_names:
			with open(output_dir+"/"+sample+"/"+sample+"_"+contig+".fasta", 'r') as file:
				line = file.readline()
				line = line.rstrip()
				x = line.split("_")
				contigLength = x[3]
				contigCov = x[5]
				sampleNameList.append(sample)
				contigNumberList.append(contigs)
				contigNameList.append(contig)
				contigLengthList.append(contigLength)
				contigCovList.append(contigCov)
		list_of_tuples = list(zip(sampleNameList, contigNumberList, contigNameList, contigLengthList, contigCovList))
		df2 = df2.append(pd.DataFrame(list_of_tuples, columns=['Sample','ContigsFound','ContigNum','ContigLength','ContigCov']), ignore_index=True)
				
	out =[out]
	df = df.append(pd.DataFrame(out, columns =['Sample','ContigsFound','LengthFinalContig','GenesAnnotated']), ignore_index=True)
	print(df)
df2.to_csv(output_dir+'/results_multiple_contigs.txt', index = False, sep = "\t")
df.to_csv(output_dir+'/results.txt', index = False, sep = "\t")
