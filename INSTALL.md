#Summary:
##For the impatient:
<pre>
	bash INSTALL.1.python_system_requirements
	bash INSTALL.2.python_requirements_globally
	echo "export PATH=$PWD/scripts:$PATH" >> $HOME/.bashrc
	export PATH=$PWD/scripts:$PATH
	cnidaria.py -h
</pre>

##To Run on Ubuntu 12 (compilation required. run before previous commands):
<pre>
bash INSTALL.3.system_compile_requirements_ubuntu_12.04
bash INSTALL.4.compile
</pre>

##To recompile on Ubuntu 14 (if you feel adventurous):
<pre>
bash INSTALL.3.system_compile_requirements
bash INSTALL.4.compile
</pre>


#For the patient:
##Before running
###Install system requirements (compulsory: requires root access)
<pre>
bash INSTALL.1.python_system_requirements
</pre>

###Install python requirements in one of two modes:
####Globally (Preferable method. requires root access):
<pre>
bash      INSTALL.2.python_requirements_globally
</pre>
####Locally (Alternative method. requires root access)
<pre>
bash      INSTALL.2.python_requirements_locally
</pre>




##Running
###Environment
- add script folder to your PATH by:
    - type, from this folder, every time you open a new terminal
<pre>
export PATH=$PWD/scripts:$PATH
</pre>

    - add (only once) cnidaria/scripts to your $HOME/.bashrc and restart (only once) your terminal
<pre>
echo "export PATH=$PWD/scripts:$PATH" >> $HOME/.bashrc
</pre>
    


##Compiling Cnidaria from source (only if necessary. requires root access)
###Before compiling
#### Ubuntu 14+
<pre>
bash INSTALL.3.system_compile_requirements
</pre>

#### Ubuntu 12
<pre>
bash INSTALL.3.system_compile_requirements_ubuntu_12.04
</pre>

###Compiling
<pre>
bash INSTALL.4.compile
</pre>



