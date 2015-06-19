import os
import sys

GCC_VER      = os.environ.get('GCC_VER', '4.8')
exe          = sys.argv[0]
exe_path_abs = os.path.abspath( exe )
exe_dir      = os.path.dirname( exe_path_abs )
venv_dir     = os.path.join( exe_dir , 'venv'     , 'lib'           )
venv_dir_c   = os.path.join( venv_dir, 'libc'+GCC_VER               )
venv_dir_p   = os.path.join( venv_dir, 'png'                        )
pack_dir     = os.path.join( venv_dir, 'python2.7', 'site-packages' )
stds         = ["/lib", "/lib64", "/usr/lib", "/usr/lib64", "/usr/local/lib", "/usr/local/lib"]

print "exe path        :", exe
print "exe abs path    :", exe_path_abs
print "exe dir         :", exe_dir
print "venv dir        :", venv_dir
print "venv dir c      :", venv_dir_c
print "venv dir png    :", venv_dir_p
print "site-package dir:", pack_dir

def add_ld(add_lib=True, add_c=True, add_png=True, add_stds=True, add_ldl=True):
    #http://stackoverflow.com/questions/6543847/setting-ld-library-path-from-inside-python
    adds  = 0
    venvs = []

    LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH', None)

    if add_lib:
        if LD_LIBRARY_PATH is None or venv_dir not in LD_LIBRARY_PATH:
            adds  += 1
            venvs += [venv_dir]

    if add_c:
        if LD_LIBRARY_PATH is None or venv_dir_c not in LD_LIBRARY_PATH:
            adds  += 1
            venvs += [venv_dir_c]

    if add_png:
        if LD_LIBRARY_PATH is None or venv_dir_p not in LD_LIBRARY_PATH:
            adds  += 1
            venvs += [venv_dir_p]

    if add_ldl and LD_LIBRARY_PATH is not None:
        venvs += LD_LIBRARY_PATH.split(":")

    if adds == 0:
        return

    if add_stds:
        venvs += stds

    os.environ['LD_LIBRARY_PATH'] = ":".join(venvs)

    try:
        print "new ld library path:", os.environ['LD_LIBRARY_PATH']
        sys.exit(0)
        os.execv(exe, sys.argv)

    except Exception, exc:
        print 'Failed re-exec:', exc
        sys.exit(1)


def add_venv():
    sys.path.insert( 0, venv_dir )
    sys.path.insert( 0, pack_dir )
    #os.environ['LD_LIBRARY_PATH'] = venv_dir + ":" + os.environ['LD_LIBRARY_PATH'] if 'LD_LIBRARY_PATH' in os.environ else venv_dir
    #print os.environ

def add_all(add_lib=True, add_c=True, add_png=True, add_stds=True, add_ldl=True):
    add_venv()
    add_ld(add_lib, add_c, add_png, add_stds, add_ldl)
