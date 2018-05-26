#!/bin/bash
MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONTAINERNAME='exercise:latest'

cd $MYDIR/../../..
docker rm $CONTAINERNAME
docker rmi $CONTAINERNAME
docker build . -f ./deploy/container/exercise/Dockerfile -t $CONTAINERNAME
