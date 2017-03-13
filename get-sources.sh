#!/bin/bash

git fetch git@github.com:llvm-mirror/clang.git release_40 --depth=1

set -e

BASE=clang
GIT_HASH=$(git rev-parse FETCH_HEAD)
SVN_ID=$(git log FETCH_HEAD --format='%b' | grep git-svn-id | awk -F"@" '{print $2}' | awk -F" " '{print $1}')

if [[ $SVN_ID == "" ]] ; then
    echo No SVN ID detected
    exit -1
fi

echo Git hash ${GIT_HASH}, SVN ${SVN_ID}

git archive --format=tar.gz FETCH_HEAD --prefix=${BASE}-$GIT_HASH/ > $GIT_HASH.tar.gz

md5sum $GIT_HASH.tar.gz > sources

cat ${BASE}.spec \
   | sed -E "s#^Release:.*\$#Release:\t1.svn${SVN_ID}%{?dist}.alonid#g"  \
   | sed -E "s#^Source0:.*\$#Source0:\thttp://llvm.org/releases/%{version}/${GIT_HASH}.tar.gz#g"  \
   | sed -E "s#^%setup -q -n ${BASE}-.*\$#%setup -q -n ${BASE}-${GIT_HASH}#g"  \
 > _temp.spec

mv _temp.spec ${BASE}.spec

