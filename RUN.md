#Running
##Environment
- add script folder to your PATH by:
    - type, from this folder, every time you open a new terminal
```
source enable.sh
```

    - add (only once) cnidaria/scripts to your $HOME/.bashrc and restart (only once) your terminal
```
echo "export PATH=$PWD/scripts:$PATH" >> $HOME/.bashrc
echo "export PATH=$PWD/src/libs/Jellyfish/bin/:$PATH" >> $HOME/.bashrc
```

#Test
enter the test folder
```
cd test
```

download the necessary fastas
```
./unpack.sh
```

run make
```
make
```

the output can be found in out/test/test

