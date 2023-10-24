#!/bin/bash

usage() {
    echo "Usage: $0 [-r] [-s] [-u] [-h]"
    echo "Options:"
    echo "  -r    Restart Docker container"
    echo "  -s    Build and run Docker container"
    echo "  -u    Stop Docker container"
    echo "  -h    Display this help message"
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

while getopts ":rsuh" opt; do
    case ${opt} in
        r)
            docker stop webshop
            docker rm webshop
            docker build -t webshop .
            docker run -d -p 8000:8000 --name webshop webshop
            ;;
        s)
            docker build -t webshop .
            docker run -d -p 8000:8000 --name webshop webshop
            ;;
        u)
            docker stop webshop
            docker rm webshop
            ;;
        h)
            usage
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done

shift $((OPTIND-1))

exit 0
