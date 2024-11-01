# Details of filtering/correcting somatic variant calls and reconstructing trees of tumor progression on 24 sublines dataset
=====================================================================================================

This file contains details about filtering and correcting somatic variant calls obtained using the existing somatic mutation callers (see Supplementary Section D of the manuscript for details of data generation and somatic mutations calling).


## Filtering and correcting variant calls
Assume that, after the variant calling step, we are given as output a matrix &#119967;<sub>*cell_id, mut_id*</sub>. In this matrix, &#119967;<sub>*cell_id, mut_id*</sub> = 1 if variant mut_id was reported to be present in subline cell_id. Similarly &#119967;<sub>*cell_id, mut_id*</sub> = 0 if mut_id was not reported in cell_id. Originally, we did not have missing entries in &#119967; (in which case, &#119967; would be set to 3). 
In addition, assume that we have also a matrix of read counts, read_counts<sub>*cell_id, mut_id*</sub> which entries are 2-tuples (variant, total). We denote these as read_counts<sub>*cell_id, mut_id*</sub>["variant"] and read_counts<sub>*cell_id, mut_id*</sub>["total"] respectively as the number of variant and total reads at the genomic position of mut_id in subline cell_id.

We first conduct the following variant filtering:
1. We remove all private mutations from &#119967; (i.e., mutations reported to be present in only one cell/subline) as these mutations are non-informative for tree reconstruction because they are always placed at a leaf corresponding to the only subline in which they are present.
2. We remove all clonal mutations from &#119967; (i.e., mutations reported to be present in all cells/sublines) as these mutations are also non-informative for tree reconstruction since they are always placed at the root of the tree.
3. To minimize the incorrect mutation calls due to misalignment and poor alignment regions, we also remove all mutations that have at least one other mutation reported within 100 basepairs of them.


To correct for false negative calls made by the mutation caller, we adjust the mutation calls in &#119967; by setting &#119967;<sub>*cell_id, mut_id*</sub> = 1 whenever read_counts<sub>*cell_id, mut_id*</sub>["variant"] >= 3 and variant allele frequency of mut_id in cell_id is at least 0.10; otherwise we set &#119967;<sub>*cell_id, mut_id*</sub> = 0. After this adjustment, some variants become either private or clonal and are removed from &#119967; for the same reasons as discussed above.

In this dataset, we expect variant allele frequency of variants to be centered around 0.50 for variants from diploid regions. For variants from regions impacted by copy number aberrations, these numbers may be lower or higher (e.g. 0.33 or 0.67 for variants from regions having 3 copies). In the original calls, we observed a subset of variants having low variant allele frequency without clear signals for copy number aberrations in regions harboring them. We suspect that these variants belong to repetitive regions or regions that are not well characterized in the mouse reference genome and thereby are hard to map reads to. In order to minimize the impact of such variants on the tree building, we removed all variants that have median variant allele frequency less than 0.25 across all sublines in which they are called. In addition, we also removed variants from low coverage regions by filtering all variants that have median coverage across all sublines less than 20. The resultant matrix D, consisting of 1689 variants, forms our (uncorrected) variant calls dataset and is available in file ./real_data_analysis/uncorrected_data/input_observed_genotype_matrix.tsv.

## Inferring tree of tumor progression
Tree of tumor progression was inferred using ScisTree (https://github.com/yufengwudcs/ScisTree) with false positive and false negative error rate priors of 0.0001 and 0.075 (these rates were obtained after grid search for different false positive and negative rates and selecting the one that yields a tree of the highest likelihood). The inferred tree is provided in the main paper (see Figure 4), whereas its newick string representation can be found in file ./real_data_analysis/uncorrected_data/output_tree_newick_string.nwk. In addition, we also provide conflict-free matrix reported by ScisTree and it is available as file  ./real_data_analysis/uncorrected_data/output_conflict_free_genotype_matrix.tsv. 

## Correcting variant calls in sublines C2, C5 and C19 and inferring tree on the corrected dataset
After running our algorithm for estimating the partition function values and analyzing weakly supported clades, we did two additional filtering steps after observing the following: 
1. Contamination of subline C19 with subline C21, most likely occurring during the sequencing library preparation. After careful inspection of variants specific to these two sublines, we observed that the vast majority of them have variant allele frequency around 0.50 in C21 and around 0.20 in C19. In addition, we conducted an additional experiment in which C19 and C21 were re-sequenced, and, while being present in the resequenced C21 subline, such variants were absent from C19 in this resequenced dataset further supporting our contamination/doublet hypothesis. To correct for these errors, for each variant mut_id reported by ScisTree as non-clonal and present in C21, we set its presence in C19, that is &#119967;<sub>*C19, mut_id*</sub>, to 0 if the number of reads supporting the variant in C19 in our resequencing experiment was less than or equal to 3.
2. We also observed that 23 mutations specific to the clade consisting of all sublines except C2 and C5 had low partition function values. After inspecting those variants we observe that 13 of them are on chromosome 3 and 8 of them are on chromosome 15, suggesting potential Loss of Heterozygosity events. Therefore we set those entries to missing in C2 and C5, i.e. &#119967;<sub>*C2, mut_id*</sub> = &#119967;<sub>*C5, mut_id*</sub> = 3 for all 23 variants.

After the above filtering steps, we again run ScisTree to obtain our corrected tree. The input provided to ScisTree and its outputs are contained in folder ./real_data_analysis/corrected_data (filenames follow the same convention as for the uncorrected data case - see section "Inferring tree of tumor progression" above for explanation). The inferred tree is also provided as Figure 5 in the main paper.  






