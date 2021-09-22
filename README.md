# slideshow-orderer
Ordering photos of a slideshow with respect to their tags (Google CodeJam 2019 Qual)

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