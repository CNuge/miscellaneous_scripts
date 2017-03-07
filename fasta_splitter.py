#!/usr/bin/env python3

#stole the following from biopython.org
def batch_iterator(iterator, batch_size):

    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.__next__()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch
            
from Bio import SeqIO

record_iter = SeqIO.parse(open("Stacks_consensus_sequences_all.fasta"),"fasta")
for i, batch in enumerate(batch_iterator(record_iter, 10000)):
    filename = "subject_group_%i.fasta" % (i + 1)
    handle = open(filename, "w")
    count = SeqIO.write(batch, handle, "fasta")
    handle.close()
    print("Wrote %i records to %s" % (count, filename))
