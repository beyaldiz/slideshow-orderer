# slideshow-orderer
Ordering photos of a slideshow with respect to their tags (Google CodeJam 2019 Qual)

## Dependencies
- Python >3.8
- tqdm

To run the solvers run main.py from the project directory as
```
python main.py --input data/{a,b,c,d,e}.txt \
               --solver {random_search, hill_climbing, genetic_algorithm} \
               --num-iters {n}
```
Example:
```
python main.py --input data/a.txt \
               --solver random_search \
               --num-iters 10000
```

## To build docker image
For amd64 architecture:
```
docker build -t slideshow-env -f docker/Dockerfile_amd64 .
```

For arm64 architecture:
```
docker build -t slideshow-env -f docker/Dockerfile_arm64 .
```

To run the docker image creating a container (this command connects the current directory to /host, all the other changes are removed)
```
docker run --rm -it --ipc=host -v $PWD:/host --network=host --name slideshow-dev slideshow-env /bin/sh -c 'cd /host; bash'
```
