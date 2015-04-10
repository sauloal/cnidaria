if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t cnidaria_make_env .

touch ok
