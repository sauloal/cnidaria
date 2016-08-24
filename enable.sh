export PATH=$PWD/scripts:$PATH
export PATH=$PWD/src/libs/Jellyfish/bin/:$PATH

if [[ -z "${LD_LIBRARY_PATH}" ]]; then
export LD_LIBRARY_PATH=$PWD/src/static
else
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$PWD/src/static
fi
