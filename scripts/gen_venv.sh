/usr/bin/virtualenv venv --always-copy
. venv/bin/activate
#wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O venv/bin/ez_setup.py
#python venv/bin/ez_setup.py
pip install -U -r requirements.txt
