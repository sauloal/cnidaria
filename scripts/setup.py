#!/usr/bin/env python
from   distutils.core      import setup
from   distutils.extension import Extension
import os
import glob


VERSION      = "0.4"
PACKAGE_NAME = "cnidariapy"

SRC_LZZ      = "src_lzz"
SRC_CPP      = "src_cpp"
SRC_OBJ      = "src_obj"
LIB_SRC      = "headers"
LIB_EXT      = "libs"

scripts = [
    "cnidaria_binomial.py",
    "cnidaria.py",
    "cnidaria_reader.py",
    "cnidaria_stats.py",
    "splitter.py"
]


cpps = [
    #"phylogenomics_shared",
    #"phylogenomics_distance",
    #"phylogenomics_binomialtree",
    #"phylogenomics",
    "jelly",
    "cnidaria"
]

os.environ["C"  ] = "g++"
os.environ["CC" ] = "g++"
os.environ["CCP"] = "g++"
os.environ["CPP"] = "g++"
os.environ["CXX"] = "g++"


#extra_compile_args = ["-std=c++0x"]
#extra_compile_args = ["-std=c++0x", "-O1"]
extra_shared_args = [
    "-std=c++11",
    "-Ofast",
    "-msse4.2",
    "-mtune=native",
    "-m64",
    "-Wall",
    "-Wno-strict-prototypes",
    "-Wno-unused-function",
    "-g"
]


#extra_shared_args = [
#    "-std=c++11",
#    "-O0",
#    "-Wno-strict-prototypes",
#    "-Wno-unused-function"
#]

extra_compile_args = ["-static"] + extra_shared_args
extra_link_args    = [         ] + extra_shared_args



for c in xrange(len(cpps)):
    cpps[c] = os.path.join( SRC_CPP, cpps[c] ) + ".cpp"

cpps.append( os.path.join( LIB_SRC, "cnidariapy.cpp" ) )

libraries      = [ "boost_system", "boost_thread", "pthread", "boost_python" ]
libraries_dirs = [ "/usr/lib/x86_64-linux-gnu" ]


includes_dirs = [
    os.path.join( LIB_EXT, "Jellyfish"         ),
    os.path.join( LIB_EXT, "Jellyfish/include" ),
    os.path.join( LIB_EXT, "rapidjson/include" ),
    os.path.join( LIB_EXT, "threadpool"        ),
    LIB_SRC,
    SRC_CPP,
    "/home/aflit001/lib/include -I/usr/include/python2.7"
]


extra_objects = []

jelly_modules = [
    'Jellyfish/lib/allocators_mmap.cc',
    'Jellyfish/lib/jsoncpp.cpp',
    'Jellyfish/lib/mer_dna.cc',
    'Jellyfish/lib/rectangular_binary_matrix.cc'
]

for c in xrange(len(jelly_modules)):
    #jelly_modules[c] = os.path.join( LIB_EXT, jelly_modules[c] )
    cpps.insert(0, os.path.join( LIB_EXT, jelly_modules[c] ) )

#for c in xrange(len(jelly_modules)):
#    print "appending ", jelly_modules[c], jelly_modules[c] + ".cc"
#    extra_objects.append( jelly_modules[c] + ".o" )
#    #extra_objects.append(
#    #    Extension( jelly_modules[c], [ jelly_modules[c] + ".cc" ] ),
#    #)



print "jelly_modules ", jelly_modules
print "extra_objects ", extra_objects

m_cnidaria = Extension(
    "cnidariapy",
    language           = "c++",
    sources            = cpps,
    libraries          = libraries,
    library_dirs       = libraries_dirs,
    include_dirs       = includes_dirs,
    extra_objects      = extra_objects,
    extra_compile_args = extra_compile_args,
    extra_link_args    = extra_link_args 
)


modules = [
    m_cnidaria,
]


setup(
    name             = PACKAGE_NAME,
    version          = VERSION,
    description      = "This is a python binding to cnidaria",
    author           = "Saulo Aflitos",
    author_email     = "sauloalves.aflitos@wur.nl",
    license          = "MIT",
    #zip_safe         = True,
    packages         = [PACKAGE_NAME],
    package_dir      = {PACKAGE_NAME: "." },
    #package_data     = {PACKAGE_NAME: ["test/*.fasta"] },
    ext_modules      = modules,
    scripts          = scripts
)
