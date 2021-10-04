import random
import itertools

class Photo:
    def __init__(self, id: int, tag_set: set):
        self.id = id
        self.tag_set = tag_set
    
    def __str__(self):
        return f"id: {self.id}, tags: {self.tag_set}"


class Data:
    def __init__(self, file):
        with open(file) as f:
            self.n = int(f.readline())
            self.photos = []
            photos_raw = f.readlines()
            for i, photo_raw in enumerate(photos_raw):
                raw_splitted = photo_raw.split()
                self.photos.append(Photo(i, set(raw_splitted[2:])))
    
    def __len__(self):
        return self.n


class Gene:
    def __init__(self, n, shuffle=False):
        self.seq = list(range(n))
        if shuffle:
            random.shuffle(self.seq)

    def __str__(self):
        return "Gene: " + str(self.seq)
    
    def __len__(self):
        return len(self.seq)

    def __lt__(self, other):
        return False


    def copy(self):
        copy_gene = Gene(len(self))
        copy_gene.seq = self.seq.copy()
        return copy_gene

    def shuffle(self):
        random.shuffle(self.seq)
    
    def swap(self, idx1, idx2):
        self.seq[idx1], self.seq[idx2] = self.seq[idx2], self.seq[idx1]
    
    def mutate(self, prob):
        alpha = random.random()
        if alpha <= prob:
            idx1, idx2 = random.randint(0, len(self.seq) - 1), random.randint(0, len(self.seq) - 1)
            self.swap(idx1, idx2)


def common_tags_n(photo1: Photo, photo2: Photo) -> int:
    return len(photo1.tag_set.intersection(photo2.tag_set))


def unique_tags_n(photo1: Photo, photo2: Photo) -> int:
    return len(photo1.tag_set.difference(photo2.tag_set))


def get_score_pair(photo1: Photo, photo2: Photo) -> int:
    return min(common_tags_n(photo1, photo2), unique_tags_n(photo1, photo2), unique_tags_n(photo2, photo1))


def get_score(data: Data, gene: Gene) -> int:
    seq = gene.seq
    photos = data.photos
    total_score = 0
    for i in range(data.n - 1):
        total_score += get_score_pair(photos[seq[i]], photos[seq[i + 1]])
    return total_score

def get_score_lr(data: Data, seq):
    photos = data.photos
    total_score = 0
    for i in range(len(seq) - 1):
        total_score += get_score_pair(photos[seq[i]], photos[seq[i + 1]])
    return total_score


def score_diff_swap(data: Data, gene: Gene, idx1: int, idx2: int):
    assert idx1 != idx2
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1
    seq = gene.seq
    photos = data.photos
    score_diff = 0
    if idx1 != 0 and idx1 + 1 != idx2:
        score_diff -= get_score_pair(photos[seq[idx1]], photos[seq[idx1 - 1]]) + get_score_pair(photos[seq[idx1]], photos[seq[idx1 + 1]])
        score_diff += get_score_pair(photos[seq[idx2]], photos[seq[idx1 - 1]]) + get_score_pair(photos[seq[idx2]], photos[seq[idx1 + 1]])
    if idx2 != len(gene) - 1 and idx1 + 1 != idx2:
        score_diff -= get_score_pair(photos[seq[idx2]], photos[seq[idx2 - 1]]) + get_score_pair(photos[seq[idx2]], photos[seq[idx2 + 1]])
        score_diff += get_score_pair(photos[seq[idx1]], photos[seq[idx2 - 1]]) + get_score_pair(photos[seq[idx1]], photos[seq[idx2 + 1]])
    if idx1 == 0 and idx1 + 1 != idx2:
        score_diff -= get_score_pair(photos[seq[idx1]], photos[seq[idx1 + 1]])
        score_diff += get_score_pair(photos[seq[idx2]], photos[seq[idx1 + 1]])
    if idx2 == len(gene) - 1 and idx1 + 1 != idx2:
        score_diff -= get_score_pair(photos[seq[idx2]], photos[seq[idx2 - 1]])
        score_diff += get_score_pair(photos[seq[idx1]], photos[seq[idx2 - 1]])
    if idx1 + 1 == idx2:
        if idx1 == 0:
            score_diff -= get_score_pair(photos[seq[idx2]], photos[seq[idx2 + 1]])
            score_diff += get_score_pair(photos[seq[idx1]], photos[seq[idx2 + 1]])
        elif idx2 == len(gene) - 1:
            score_diff -= get_score_pair(photos[seq[idx1]], photos[seq[idx1 - 1]])
            score_diff += get_score_pair(photos[seq[idx2]], photos[seq[idx1 - 1]])
        else:
            score_diff -= get_score_pair(photos[seq[idx2]], photos[seq[idx2 + 1]]) + get_score_pair(photos[seq[idx1]], photos[seq[idx1 - 1]])
            score_diff += get_score_pair(photos[seq[idx1]], photos[seq[idx2 + 1]]) + get_score_pair(photos[seq[idx2]], photos[seq[idx1 - 1]])
    return score_diff


def order_crossover(gene1: Gene, gene2: Gene):
    n = len(gene1)
    ind1 = random.randint(0, n - 1)
    ind2 = random.randint(0, n - 1)

    if ind1 > ind2:
        ind1, ind2 = ind2, ind1

    offspring1 = gene1.copy()
    offspring2 = gene2.copy()

    used = [False for _ in range(n)]

    for i in range(ind1, ind2 + 1):
        used[offspring1.seq[i]] = True
    
    ptr = ind2
    for i in range(n):
        ind = (i + ind2 + 1) % n
        val = gene2.seq[ind]
        if not used[val]:
            ptr = (ptr + 1) % n
            offspring1.seq[ptr] = val
            used[val] = True
    
    used = [False for _ in range(n)]

    for i in range(ind1, ind2 + 1):
        used[offspring2.seq[i]] = True
    
    ptr = ind2
    for i in range(n):
        ind = (i + ind2 + 1) % n
        val = gene1.seq[ind]
        if not used[val]:
            ptr = (ptr + 1) % n
            offspring2.seq[ptr] = val
            used[val] = True
    
    return offspring1, offspring2


def get_opt(data: Data, gene: Gene, idx1, idx2):
    in1, in2 = idx1, idx2
    if idx1 != 0:
        in1 -= 1
    if idx2 == data.n:
        in2 -= 1
    opt_score = get_score_lr(data, gene.seq[in1: in2 + 1])
    opt_slc = gene.seq[idx1: idx2]
    diff = 0
    for perm in itertools.permutations(gene.seq[idx1: idx2], idx2 - idx1):
        perm_pad = perm
        if idx1 != 0:
            perm_pad = tuple([gene.seq[idx1 - 1]]) + perm_pad
        if idx2 != data.n:
            perm_pad = perm_pad + tuple([gene.seq[idx2]])
        perm_score = get_score_lr(data, perm_pad)
        if perm_score > opt_score:
            diff += perm_score - opt_score
            opt_score = perm_score
            opt_slc = perm
    return list(opt_slc), diff

    
def window_mutate(data: Data, gene: Gene, window_size, stride):
    assert window_size <= 10
    score_diff = 0
    for i in range(0, len(gene) - window_size + 1, stride):
        opt_slc, diff = get_opt(data, gene, i, i + window_size)
        gene.seq[i: i + window_size] = opt_slc
        score_diff += diff
    return score_diff

    
def test():
    a = Data("data/example_data.txt")
    b = Gene(a.n, shuffle=True)
    print(get_score(a, b))
    print(b)
    print(window_mutate(a, b, 2, 1))
    print(b)
    print(get_score(a, b))
    
    # maxi = 0
    # for i in range(30):
    #     if i % 10 == 0:
    #         print(i)
    #     maxi = max(maxi, get_score(a, b))
    #     b.shuffle()
    # print(maxi)


if __name__ == "__main__":
    test()