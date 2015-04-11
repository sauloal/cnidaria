if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t sauloal/cnidaria_make_env .

touch ok
