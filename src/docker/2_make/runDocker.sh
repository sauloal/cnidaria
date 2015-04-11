if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t sauloal/cnidaria_make .

docker run --rm -it --name cnidaria_making -v $PWD/../../:/data sauloal/cnidaria_make

touch ok
