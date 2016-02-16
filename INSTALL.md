#Summary:
**Cnidaria comes pre-compiled. No installation or compilation required.**




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
```



# Compiling (!Not necessary!)
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**
**NOT NECESSARY**

If you still want to do so:


##To recompile on Ubuntu 12:
```
bash INSTALL.md.4.system_compile_requirements_ubuntu_12.04
bash INSTALL.md.1.compile
```

##To recompile on Ubuntu 14:
```
bash INSTALL.md.3.system_compile_requirements
bash INSTALL.md.4.compile
```

then:
```
bash INSTALL.md.2.python_system_requirements
bash INSTALL.md.3.python_requirements_globally
echo "export PATH=$PWD/scripts:$PATH" >> $HOME/.bashrc
export PATH=$PWD/scripts:$PATH
cnidaria.py -h
```

