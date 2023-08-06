"""Main module."""

import pandas as pd
import pysam as ps
import sys
import os


def check_mutation_file_matches_ref_genome(
    ref_fasta_path: str,
    mutation_file: str,
    col_chromosome: str = "Chromosome",
    col_start_position: str = "Start_Position",
    col_ref_allele: str = "Reference_Allele",
    position_is_zero_based: bool = False
):
    """
    Description. Test whether a mutation file was actually called against a particular reference genome. This function compares reference alleles in mutation files to the actual base at the position of a user-supplied reference genome. Any mismatches means it is unlikely that the coords in the mutational file correspond to the supplied reference genome.

    :param ref_fasta_path: Path to fasta file (should have fai index in same directory)
    :param mutation_file: A tabular file with a header (defaults designed for MAF but can use any tabular format as long as the following paramaters are customised)
    :param col_chromosome: Name of the column describing the  chromosome of mutation
    :param col_start_position: Name of the column describing the start position of the mutation
    :param col_ref_allele: Name of the column describing the reference allele of the mutation
    :param position_is_zero_based: Is the start position of zero based or one based?
    :return: a dataframe describing each mutation and whether or not it matched the reference genome supplied
    """
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
    sys.stderr.write(str(mutations_after_filtration) + "/" + str(
        mutations_before_filtration) + " mutations will be used to test how well the mutation file matches against the reference\n")

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

# bob = check_mutation_file_matches_ref_genome("/Users/selkamand/Documents/IGV/genomes/seq/hg19.fasta", "/Users/selkamand/projects/python_packages/easyaspymutations/data/TCGA.KIRP.muse.97c1698f-d4a0-4bb0-949b-92e59011f438.DR-10.0.somatic.maf.gz","maf")
# bob2 = check_mutation_file_matches_ref_genome("/Users/selkamand/Documents/IGV/genomes/seq/hg38.fa", "/Users/selkamand/projects/python_packages/easyaspymutations/data/TCGA.KIRP.muse.97c1698f-d4a0-4bb0-949b-92e59011f438.DR-10.0.somatic.maf.gz","maf")
