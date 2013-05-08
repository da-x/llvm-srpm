#!/bin/sh

DIRNAME=compiler-rt-$( date +%Y%m%d )
URL=http://llvm.org/git/compiler-rt.git

rm -rf $DIRNAME
git clone $URL $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git log | head -1
else
    git checkout $1
fi
git log | head -1 | awk '{ print $2 }' > ../commitid
rm -rf .git
cd ..
tar cf - $DIRNAME | xz -c9 > $DIRNAME.tar.xz
rm -rf $DIRNAME
