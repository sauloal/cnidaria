set -xeu

if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t sauloal/cnidaria_run .

touch ok
