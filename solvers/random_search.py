from tqdm import tqdm


from tools.utils import Data, Gene, get_score


class RandomSearch:
    def __init__(self, data: Data, num_iters: int):
        self.gene = Gene(data.n)
        self.data = data
        self.num_iters = num_iters
        self.best_gene = None
        self.best_score = 0
    
    def run(self):
        with tqdm(range(self.num_iters)) as pbar:
            for i in pbar:
                self.gene.shuffle()
                score = get_score(self.data, self.gene)
                if self.best_score < score:
                    self.best_score = score
                    self.best_gene = self.gene
                pbar.set_postfix({"Score": self.best_score})
