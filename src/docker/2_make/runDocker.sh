if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t cnidaria_make .

docker run --rm -it --name cnidaria_making -v $PWD/../../:/data cnidaria_make

touch ok
