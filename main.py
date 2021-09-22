import argparse

from tools.utils import Data

from solvers.random_search import RandomSearch


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                         default="data/c_memorable_moments.txt", help="Input file")
    parser.add_argument('--solver', type=str,
                         default="random_search", help="Solver to use")
    parser.add_argument('--num-iters', type=int,
                         default=100, help="Number of iterations")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    data = Data(args.input)
    solver = None
    
    if args.solver == "random_search":
        solver = RandomSearch(data, args.num_iters)
    
    if solver == None:
        raise NotImplementedError

    solver.run()


if __name__ == "__main__":
    main()
