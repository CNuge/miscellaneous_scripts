
""" note this is still a work in progress, ill update docs fully at the end """

these scripts are written to take the information from a .vcf file on the position of
snps within a genome, and a genome fasta file and use these inputs to build the files
necessary for the design of an Affymetrix Axiom® myDesign^TM Array.

the process requries a snp to be placed at the 36th base pair of a 71bp sequence,
and for certain other pieces of informaiton to be included in a tab delimited dataframe

see:
https://wabi-wiki.scilifelab.se/download/attachments/16941466/DNA01619-3%20Tech%20note%20Axiom%20Agrigeno_myDesign%20SNP%20submission.pdf?api=v2
for the documentation from Affymetrix
