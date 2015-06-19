import os
import sys

GCC_VER      = os.environ.get('GCC_VER', '4.8')
exe          = sys.argv[0]
exe_path_abs = os.path.abspath( exe )
exe_dir      = os.path.dirname( exe_path_abs )
venv_dir     = os.path.join( exe_dir , 'venv'     , 'lib'           )
venv_dir_c   = os.path.join( venv_dir, 'libc'+GCC_VER               )
pack_dir     = os.path.join( venv_dir, 'python2.7', 'site-packages' )

print "exe path        :", exe
print "exe abs path    :", exe_path_abs
print "exe dir         :", exe_dir
print "venv dir        :", venv_dir
print "venv dir c      :", venv_dir_c
print "site-package dir:", pack_dir

def add_ld():
    #http://stackoverflow.com/questions/6543847/setting-ld-library-path-from-inside-python
    if 'LD_LIBRARY_PATH' not in os.environ:
        #print "NO LD IN ENV. RESTARTING", os.environ
        os.environ['LD_LIBRARY_PATH'] = "%s" % ":".join("/lib","/lib64","/usr/lib","/usr/lib64","/usr/local/lib","/usr/local/lib",venv_dir, venv_dir_c)
        try:
            os.execv(exe, sys.argv)

        except Exception, exc:
            print 'Failed re-exec:', exc
            sys.exit(1)
    else:
        print "LD PRESENT IN ENV. RESUMING"#, os.environ['LD_LIBRARY_PATH']


def add_venv():
    sys.path.insert( 0, venv_dir )
    sys.path.insert( 0, pack_dir )
    #os.environ['LD_LIBRARY_PATH'] = venv_dir + ":" + os.environ['LD_LIBRARY_PATH'] if 'LD_LIBRARY_PATH' in os.environ else venv_dir
    #print os.environ

def add_all():
    add_ld()
    add_venv()
