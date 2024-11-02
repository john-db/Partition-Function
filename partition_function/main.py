import pandas as pd
import argparse
import _partition_function
from _partition_function import partition_function
from decimal import Decimal

def main(args):
    path = args.input_matrix
    df = pd.read_table(path, index_col=0)
    
    alpha=args.alpha
    beta=args.beta

    divide = True
    num_samples = args.num_samples
    delta = 0.8
    eps = 10.0
    coef = 10
    seed = args.seed

    output = "number of samples = " + str(num_samples) + "\n"
    cells = sorted(args.cells.split(","))

    muts = [args.mutation]

    names_to_cells = list(df.index)

    pf = partition_function(df_input=df, alpha=alpha, beta=beta, n_samples=num_samples, n_batches=1, muts=muts, cells=cells, names_to_cells=names_to_cells,eps = eps, delta=delta, divide=divide, coef=coef, my_seed=seed)

    num = pf[0].iloc[0][0]
    denom = pf[0].iloc[0][1]


    output = "Input: " + args.input_matrix + "\n"
    output += "False-positive rate: " + str(args.alpha) + "\n"
    output += "False-negative rate: " + str(args.beta) + "\n"
    output += "Clade: " + ",".join(cells) + "\n"
    output += "Mutation: "  + args.mutation + "\n"
    output += "Number of samples: " + str(args.num_samples) + "\n"
    output += "RNG seed: " + str(seed) + "\n"
    output += "numerator_est: " + str(num) + "\n"
    output += "denominator_est: " + str(denom) + "\n"
    output += "Partition function estimate: " + str(float(Decimal(num / denom)))
    print(output)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run.py')

    parser.add_argument("-i", "--input_matrix", type=str,                                                        
                        help="Path to input genotype matrix where rows correspond to cells/sublines and columns correspond to mutations. See repo examples for formatting.", required=True)
    parser.add_argument("-n", "--num_samples", type=int,                                                        
                        help="Number of trees to be sampled", required=True)
    parser.add_argument("-c", "--cells", type=str,                                                        
                        help="List of cells (comma separated)", required=True)
    parser.add_argument("-m", "--mutation", type=str,                                                        
                        help="Name of the mutation (column) in the matrix", required=True)
    parser.add_argument("-fp", "--alpha", type=float,                                                        
                        help="False-positive rate (alpha in the paper)", required=True)
    parser.add_argument("-fn", "--beta", type=float,                                                        
                        help="False-negative rate (beta in the paper)", required=True)
    parser.add_argument("-s", "--seed", type=int,                                                        
                        help="random seed", required=False, default=0)
    
    
    main(parser.parse_args())
