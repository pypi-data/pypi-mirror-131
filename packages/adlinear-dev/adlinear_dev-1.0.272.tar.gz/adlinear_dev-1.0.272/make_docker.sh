docker build . -t adlinear
docker tag adlearnhpcprod eu.gcr.io/second-capsule-253207/adlinear:latest
docker push eu.gcr.io/second-capsule-253207/adlinear:latest