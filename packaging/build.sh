#!/bin/sh
mkdir -p debian/usr/lib/python2.5/site-packages/flow
cd ../src && find . -name '*.py' | cpio -pvmud ../packaging/debian/usr/lib/python2.5/site-packages/flow
cd -
mkdir -p debian/usr/lib/python2.5/site-packages/flow/obo
cp ../src/obo/cell.obo debian/usr/lib/python2.5/site-packages/flow/obo
echo 'copy bayes.so to debian/usr/lib/python2.5/site-packages/flow/plugins/statistics/Bayes/'
echo 'copy flow.so to debian/usr/lib/python2.5/site-packages/flow/plugins/statistics/Kde/'
echo 'then run dpkg-deb --build debian'

