import argparse

from tools.utils import Data

from solvers.random_search import RandomSearch
from solvers.hill_climbing import HillClimbing 
from solvers.genetic_algorithm import GeneticAlgorithm


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                         default="data/d.txt", help="Input file")
    parser.add_argument('--solver', type=str,
                         default="random_search", help="Solver to use")
    parser.add_argument('--num-iters', type=int,
                         default=1000000, help="Number of iterations")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    data = Data(args.input)
    solver = None
    
    if args.solver == "random_search":
        solver = RandomSearch(data, args.num_iters)
    
    if args.solver == "hill_climbing":
        solver = HillClimbing(data, args.num_iters)
    
    if args.solver == "genetic_algorithm":
        solver = GeneticAlgorithm(data, 20, [], 3, 0.1, args.num_iters)
    
    if args.solver == "combined":
        pops = []
        for i in range(10):
            solver = HillClimbing(data, 10000, 1000, 4, 3)
            solver.run()
            pops.append((solver.best_gene))
        solver = GeneticAlgorithm(data, 40, pops, 3, 0.1, args.num_iters)
        solver.run()
    
    if solver == None:
        raise NotImplementedError

    solver.run()


if __name__ == "__main__":
    main()
