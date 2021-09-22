import random


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


class Gene:
    def __init__(self, n, shuffle=False):
        self.seq = list(range(n))
        if shuffle:
            random.shuffle(self.seq)

    def __str__(self):
        return "Gene: " + str(self.seq)
    
    def shuffle(self):
        random.shuffle(self.seq)


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


def test():
    a = Data("data/inputs/b_lovely_landscapes.txt")
    b = Gene(a.n, shuffle=True)

    maxi = 0
    for i in range(30):
        if i % 10 == 0:
            print(i)
        maxi = max(maxi, get_score(a, b))
        b.shuffle()
    print(maxi)


def main():
    test()


if __name__ == "__main__":
    main()