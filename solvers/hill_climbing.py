import random
import itertools

from tqdm import tqdm

from tools.utils import Data, Gene, get_score, score_diff_swap, window_mutate


class HillClimbing:
    def __init__(self, data: Data, num_iters: int):
        self.gene = Gene(data.n, shuffle=True)
        self.data = data
        self.num_iters = num_iters
        self.score = get_score(self.data, self.gene)
        self.best_score = 0
        self.best_gene = None

    def run(self):
        with tqdm(total=self.num_iters) as pbar:
            for iter_cnt, (idx1, idx2) in enumerate(itertools.islice(itertools.cycle(itertools.combinations(range(self.data.n), 2)), self.num_iters)):
                score_diff = score_diff_swap(self.data, self.gene, idx1, idx2)
                if score_diff > 0:
                    self.gene.swap(idx1, idx2)
                    self.score += score_diff
                pbar.update(1)
                pbar.set_postfix({"Score": self.score})
        self.best_gene = self.gene
        self.best_score = self.score
        assert self.best_score == get_score(self.data, self.gene)


def main():
    data = Data("data/a.txt")
    solver = HillClimbing(data, 10)
    solver.run()


if __name__ == "__main__":
    main()