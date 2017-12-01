#!/bin/bash

spec_name=clang

get_and_patch() {
    set -e

    repo_name=$1
    arch_name=$2
    tar_name=$3

    git fetch git@github.com:llvm-mirror/${repo_name}.git release_50 --depth=1

    GIT_HASH=$(git rev-parse FETCH_HEAD)
    SVN_ID=$(git log FETCH_HEAD --format='%b' | grep git-svn-id | awk -F"@" '{print $2}' | awk -F" " '{print $1}')

    if [[ $SVN_ID == "" ]] ; then
	echo No SVN ID detected
	exit -1
    fi

    echo Git hash ${GIT_HASH}, SVN ${SVN_ID}

    git archive --format=tar.gz FETCH_HEAD --prefix=${tar_name}-$GIT_HASH/ > ${tar_name}-$GIT_HASH.tar.gz
    set +e
    git branch -D __temp_save_${repo_name} 2> /dev/null
    set -e
    git branch __temp_save_${repo_name} FETCH_HEAD

    cat ${spec_name}.spec \
	| sed -E "s#(^[%]define h_${arch_name} ).*#\1${GIT_HASH}#g"  \
	> _temp.spec
    mv _temp.spec ${spec_name}.spec

    eval ${arch_name}_svn=$SVN_ID
}

get_and_patch clang cfe cfe
get_and_patch clang-tools-extra clang_tools_extra clang-tools-extra
get_and_patch test-suite test_suite test-suite

cat ${spec_name}.spec \
    | sed -E "s#^Release:.*\$#Release:\t1.svn${cfe_svn}%{?dist}.alonid#g"  \
    > _temp.spec
mv _temp.spec ${spec_name}.spec

