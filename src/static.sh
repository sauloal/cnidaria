cp /usr/lib/x86_64-linux-gnu/libboost_filesystem.a static/
cp /usr/lib/x86_64-linux-gnu/libboost_system.a static/
cp /usr/lib/x86_64-linux-gnu/libboost_thread.a static/
cp /usr/lib/x86_64-linux-gnu/librt.a static/
cp /usr/lib/x86_64-linux-gnu/libpthread.a static/
cp /usr/lib/x86_64-linux-gnu/libm.a static/

cp /usr/lib/x86_64-linux-gnu/libboost_filesystem.so static
cp /usr/lib/x86_64-linux-gnu/libboost_system.so static
cp /usr/lib/x86_64-linux-gnu/libboost_thread.so static
cp /usr/lib/x86_64-linux-gnu/librt.so static
cp /usr/lib/x86_64-linux-gnu/libpthread.so static
cp /usr/lib/x86_64-linux-gnu/libm.so static/


cp /usr/lib/x86_64-linux-gnu/libboost_python*.so static
cp /usr/lib/x86_64-linux-gnu/libboost_python*.a static

cp /usr/lib/x86_64-linux-gnu/libpython2.7.a static
cp /usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0 static
cp /usr/lib/x86_64-linux-gnu/libpython3.4m.a static
cp /usr/lib/x86_64-linux-gnu/libpython3.4m.so.1.0 static


cd static

ln -s libboost_filesystem.so  libboost_filesystem.so.1.54.0
ln -s libboost_python-py27.a  libboost_python.a
ln -s libboost_python-py27.so libboost_python-py27.so.1.54.0
ln -s libboost_python-py34.so libboost_python-py34.so.1.54.0
ln -s libboost_python-py27.so libboost_python.so
ln -s libboost_system.so      libboost_system.so.1.54.0
ln -s libboost_thread.so      libboost_thread.so.1.54.0
ln -s libpython2.7.so.1.0     libpython2.7.so.1
ln -s libpython2.7.so.1.0     libpython2.7.so
ln -s libpython3.4m.so.1.0    libpython3.4m.so.1
ln -s libpython3.4m.so.1.0    libpython3.4m.so


