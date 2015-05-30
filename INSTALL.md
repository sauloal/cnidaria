#Before running
<pre>
sudo bash INSTALL.1.python_system_requirements
bash      INSTALL.2.python_requirements
</pre>

#Running
##Environment
- add script folder to your PATH
    - you can:
        - type, from this folder, every time you open a new terminal
<pre>
export PATH=$PWD/scripts:$PATH
</pre>

        - add once to your .bashrc and restart your terminal once
<pre>
echo "export PATH=$PWD/scripts:$PATH" >> ~/.bashrc
</pre>
    

#Compiling
##For compiling (if necessary) - Ubuntu 14+
<pre>
sudo bash INSTALL.3.system_compile_requirements
</pre>

##For compiling (if necessary) - Ubuntu 12
<pre>
sudo bash INSTALL.3.system_compile_requirements_ubuntu_12.04
</pre>

##Compiling
<pre>
bash INSTALL.4.compile
</pre>



