set -xeu

if [[ -f "ok" ]]; then
exit 0
fi

docker rmi sauloal/cnidaria_full || true

docker build --rm --build-arg USER_UID=`id -u $USER` -t sauloal/cnidaria_full .

touch ok
