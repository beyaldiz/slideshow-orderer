from tools.utils import Data, Gene, get_score

class RandomSearch:
    def __init__(self, data: Data, num_iters: int):
        self.gene = Gene(data.n)
        self.data = data
        self.num_iters = num_iters
        self.best_gene = None
        self.best_score = 0
    
    def run(self):
        for i in range(self.num_iters):
            self.gene.shuffle()
            score = get_score(self.data, self.gene)
            if self.best_score < score:
                self.best_score = score
                self.best_gene = self.gene
