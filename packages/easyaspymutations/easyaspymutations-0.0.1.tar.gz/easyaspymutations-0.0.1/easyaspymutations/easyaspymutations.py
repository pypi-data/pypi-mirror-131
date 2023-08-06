"""Main module."""

import pandas as pd
import pysam as ps
import sys
import os

def reference_guesser(
    ref_fasta_path: str,
    mutation_file: str,
    filetype: object,
    col_chromosome: str = "Chromosome",
    col_start_position: str = "Start_Position",
    col_ref_allele: str = "Reference_Allele",
    position_is_zero_based: bool = False
):
    # Read in files
    sys.stderr.write("------- Configuration -------\n")
    sys.stderr.write("Reference Genome: " + os.path.basename(ref_fasta_path) + '\n')
    sys.stderr.write("Chromosome Column: " + col_chromosome + '\n')
    sys.stderr.write("Start Position Column: " + col_start_position + '\n')
    sys.stderr.write("Reference Allele Column: " + col_ref_allele + '\n')
    sys.stderr.write("Zero Based: " + str(position_is_zero_based) + '\n\n')

    ref_fasta = ps.FastaFile(filename=ref_fasta_path)

    mutations = pd.read_csv(
        mutation_file,
        sep='\t',
        comment='#',
        usecols=[col_chromosome, col_start_position, col_ref_allele]
    )

    mutations_before_filtration = len(mutations.index)

    # Filter For entries with a single reference allele thats either A, C, T or G
    mutations[col_ref_allele] = mutations[col_ref_allele].str.upper()
    mutations = mutations[mutations[col_ref_allele].str.upper().isin(["A", "C", "T", "G"])]
    mutations_after_filtration = len(mutations.index)
    sys.stderr.write(str(mutations_after_filtration) + "/" + str(mutations_before_filtration) + " mutations will be used to test how well the mutation file matches against the reference\n")

    mutations["samtools_region"] = mutations.apply(
        lambda df: str(df[col_chromosome]) + ":" +
                   str(df[col_start_position] + position_is_zero_based) + '-' +
                   str(df[col_start_position] + position_is_zero_based),
        axis=1)

    mutations['actual_ref_allele'] = mutations["samtools_region"].apply(lambda x: ref_fasta.fetch(region=x)).str.upper()
    mutations['ref_matches'] = mutations.apply(lambda df: df["actual_ref_allele"] == df[col_ref_allele], axis=1)
    times_ref_allele_matched = mutations['ref_matches'].sum()
    times_ref_allele_didnt_match = mutations_after_filtration - times_ref_allele_matched

    sys.stderr.write(
        str(times_ref_allele_didnt_match) + '/' + str(mutations_after_filtration) +
        ' mismatches with reference genome\n\n'
    )

    if times_ref_allele_didnt_match == 0 and mutations_after_filtration > 5:
        sys.stderr.write('Perfect Match! (' + os.path.basename(ref_fasta_path) + ')\n\n')

    return mutations


#bob = reference_guesser("/Users/selkamand/Documents/IGV/genomes/seq/hg19.fasta", "/Users/selkamand/projects/python_packages/easyaspymutations/data/TCGA.KIRP.muse.97c1698f-d4a0-4bb0-949b-92e59011f438.DR-10.0.somatic.maf.gz","maf")
#bob2 = reference_guesser("/Users/selkamand/Documents/IGV/genomes/seq/hg38.fa", "/Users/selkamand/projects/python_packages/easyaspymutations/data/TCGA.KIRP.muse.97c1698f-d4a0-4bb0-949b-92e59011f438.DR-10.0.somatic.maf.gz","maf")

def my_function():
    print("Hello from a function")
