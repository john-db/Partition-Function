# Details of files related to the bootstrapping experiments

This folder contains bootstrapping samples for uncorrected and corrected 24 sublines dataset (for more details see ./real_data_analyis folder, as well as the manuscript). 

For each dataset, we did 200 bootstrap replicates. For each of them, we provide input genotype matrix in the format used in this work (i.e., ternary observed genotype matrix). For example, file D-no_correction-br137.tsv represents 137-th matrix (obtained by sampling mutations with replacement from the matching observed genotype matrix). In addition, we also made available inputs provided to ScisTree, which follow input format specifications of this tool. For example, for the 137-th bootstrap sample in the uncorrected data the file provided as input to ScisTree is be D-no_correction-br137scistree_format.tsv.

Lastly, the trees inferred by ScisTree are listed in no_correction_bootstraps.nwks and C19_and_C2C5_corrected_bootstraps.nwks, each file consisting of 200 lines (one tree per line provided in newick format). 
