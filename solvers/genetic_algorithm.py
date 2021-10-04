import random
import itertools
import heapq

from tqdm import tqdm

from tools.utils import Data, Gene, order_crossover, get_score, score_diff_swap, window_mutate


class GeneticAlgorithm:
    def __init__(self, data: Data, population_size: int, initial_population: list,
                 tournament_k: int, mutation_prob: float, num_iters: int):
        self.data = data
        self.p_size = population_size
        self.p = [(get_score(data, gene), gene) for gene in initial_population]
        for i in range(population_size - len(initial_population)):
            rand_gene = Gene(self.data.n, shuffle=True)
            self.p.append((get_score(self.data, rand_gene), rand_gene))
        heapq.heapify(self.p)
        self.tk = tournament_k
        self.mutation_prob = mutation_prob
        self.num_iters = num_iters
        self.best_score = max(self.p)[0]
        self.best_gene = max(self.p)[1]

    def get_parent(self):
        best_par = max(random.sample(self.p, self.tk))
        return best_par
    
    def run(self):
        with tqdm(total=self.num_iters) as pbar:
            for iter in range(self.num_iters):
                p1, p2 = self.get_parent(), self.get_parent()
                c1, c2 = order_crossover(p1[1], p2[1])
                c1.mutate(self.mutation_prob)
                c2.mutate(self.mutation_prob)

                score1, score2 = get_score(self.data, c1), get_score(self.data, c2)
                if self.best_score < score1:
                    self.best_score = score1
                    self.best_gene = c1.copy()
                if self.best_score < score2:
                    self.best_score = score2
                    self.best_gene = c2.copy()
                
                heapq.heappushpop(self.p, (score1, c1))
                heapq.heappushpop(self.p, (score2, c2))

                pbar.update(1)
                pbar.set_postfix({"Score": self.best_score})
        assert self.best_score == get_score(self.data, self.best_gene)


def main():
    data = Data("data/d.txt")
    solver = GeneticAlgorithm(data, 10, [], 3, 0.1, 10)
    solver.run()
    pass


if __name__ == "__main__":
    main()