%global clang_tools_binaries \
	%{_bindir}/clang-apply-replacements \
	%{_bindir}/clang-change-namespace \
	%{_bindir}/clang-include-fixer \
	%{_bindir}/clang-query \
	%{_bindir}/clang-reorder-fields \
	%{_bindir}/clang-rename \
	%{_bindir}/clang-tidy

%global clang_binaries \
	%{_bindir}/clang \
	%{_bindir}/clang++ \
	%{_bindir}/clang-4.0 \
	%{_bindir}/clang-check \
	%{_bindir}/clang-cl \
	%{_bindir}/clang-cpp \
	%{_bindir}/clang-format \
	%{_bindir}/clang-import-test \
	%{_bindir}/clang-offload-bundler

Name:		clang
Version:	4.0.0
Release:	2%{?dist}
Summary:	A C language family front-end for LLVM

License:	NCSA
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.xz
Source1:	http://llvm.org/releases/%{version}/clang-tools-extra-%{version}.src.tar.xz

Source100:	clang-config.h

Patch0:		0001-CMake-Fix-pthread-handling-for-out-of-tree-builds.patch

BuildRequires:	cmake
BuildRequires:	llvm-devel = %{version}
BuildRequires:	libxml2-devel
BuildRequires:  llvm-static = %{version}
BuildRequires:  perl-generators
BuildRequires:  ncurses-devel
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# clang requires gcc, clang++ requires libstdc++-devel
# - https://bugzilla.redhat.com/show_bug.cgi?id=1021645
# - https://bugzilla.redhat.com/show_bug.cgi?id=1158594
Requires:	libstdc++-devel
Requires:	gcc-c++


%description
clang: noun
    1. A loud, resonant, metallic sound.
    2. The strident call of a crane or goose.
    3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extensible.

%package libs
Summary: Runtime library for clang
Requires: compiler-rt%{?_isa} >= %{version}

%description libs
Runtime library for clang.

%package devel
Summary: Development header files for clang.
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development header files for clang.

%package analyzer
Summary:	A source code analysis framework
License:	NCSA and MIT
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}
# not picked up automatically since files are currently not installed in
# standard Python hierarchies yet
Requires:	python

%description analyzer
The Clang Static Analyzer consists of both a source code analysis
framework and a standalone tool that finds bugs in C and Objective-C
programs. The standalone tool is invoked from the command-line, and is
intended to run in tandem with a build of a project or code base.

%package tools-extra
Summary: Extra tools for clang
Requires: llvm-libs%{?_isa} = %{version}
Requires: clang-libs%{?_isa} = %{version}

%description tools-extra
A set of extra tools built using Clang's tooling API.

%prep
%setup -T -q -b 1 -n clang-tools-extra-%{version}.src
%patch0 -p1 -b .pthread-fix
%setup -q -n cfe-%{version}.src

mv ../clang-tools-extra-%{version}.src tools/extra

%build
mkdir -p _build
cd _build
%cmake .. \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DLLVM_CONFIG:FILEPATH=/usr/bin/llvm-config-%{__isa_bits} \
	\
	-DCLANG_ENABLE_ARCMT:BOOL=ON \
	-DCLANG_ENABLE_STATIC_ANALYZER:BOOL=ON \
	-DCLANG_INCLUDE_DOCS:BOOL=ON \
	-DCLANG_INCLUDE_TESTS:BOOL=OFF \
	-DCLANG_PLUGIN_SUPPORT:BOOL=ON \
	-DENABLE_LINKER_BUILD_ID:BOOL=ON \
	\
	-DCLANG_BUILD_EXAMPLES:BOOL=OFF \
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64 \
%else
        -DLLVM_LIBDIR_SUFFIX= \
%endif
	-DLIB_SUFFIX=

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# multilib fix
mv -v %{buildroot}%{_includedir}/clang/Config/config{,-%{__isa_bits}}.h
install -m 0644 %{SOURCE100} %{buildroot}%{_includedir}/clang/Config/config.h

# remove git integration
rm -vf %{buildroot}%{_bindir}/git-clang-format
# remove editor integrations (bbedit, sublime, emacs, vim)
rm -vf %{buildroot}%{_datadir}/clang/clang-format-bbedit.applescript
rm -vf %{buildroot}%{_datadir}/clang/clang-format-sublime.py*
rm -vf %{buildroot}%{_datadir}/clang/clang-format.el
rm -vf %{buildroot}%{_datadir}/clang/clang-format.py*
# clang-tools-extra
rm -vf %{buildroot}%{_datadir}/clang/clang-include-fixer.py
rm -vf %{buildroot}%{_datadir}/clang/clang-tidy-diff.py
rm -vf %{buildroot}%{_datadir}/clang/run-clang-tidy.py
rm -vf %{buildroot}%{_datadir}/clang/run-find-all-symbols.py
rm -vf %{buildroot}%{_datadir}/clang/clang-include-fixer.el
rm -vf %{buildroot}%{_datadir}/clang/clang-rename.el
rm -vf %{buildroot}%{_datadir}/clang/clang-rename.py
# remove diff reformatter
rm -vf %{buildroot}%{_datadir}/clang/clang-format-diff.py*

%check
# requires lit.py from LLVM utilities
#cd _build
#make check-all

%files
%{_libdir}/clang/
%{clang_binaries}
%{_bindir}/c-index-test

%files libs
%{_libdir}/*.so.*
%{_libdir}/*.so

%files devel
%{_includedir}/clang/
%{_includedir}/clang-c/
%{_libdir}/cmake/
%dir %{_datadir}/clang/

%files analyzer
%{_bindir}/scan-view
%{_bindir}/scan-build
%{_bindir}/scan-build
%{_libexecdir}/ccc-analyzer
%{_libexecdir}/c++-analyzer
%{_datadir}/scan-view/
%{_datadir}/scan-build/
%{_mandir}/man1/scan-build.1.*

%files tools-extra
%{clang_tools_binaries}
%{_bindir}/find-all-symbols
%{_bindir}/modularize

%changelog
* Fri Mar 24 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-2
- Fix clang-tools-extra build
- Fix install

* Thu Mar 23 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- clang 4.0.0 final release

* Mon Mar 20 2017 David Goerger <david.goerger@yale.edu> - 3.9.1-3
- add clang-tools-extra rhbz#1328091

* Thu Mar 16 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-2
- Enable build-id by default rhbz#1432403

* Thu Mar 02 2017 Dave Airlie <airlied@redhat.com> - 3.9.1-1
- clang 3.9.1 final release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3.9.0-3
- Add Requires: compiler-rt to clang-libs.
- Without this, compiling with certain CFLAGS breaks.

* Tue Nov  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 3.9.0-2
- Rebuild for new arches

* Fri Oct 14 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-1
- clang 3.9.0 final release

* Fri Jul 01 2016 Stephan Bergmann <sbergman@redhat.com> - 3.8.0-2
- Resolves: rhbz#1282645 add GCC abi_tag support

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- clang 3.8.0 final release

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.4
- clang 3.8.0rc3

* Wed Feb 24 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-0.3
- package all libs into clang-libs.

* Wed Feb 24 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.2
- enable dynamic linking of clang against llvm

* Thu Feb 18 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-0.1
- clang 3.8.0rc2

* Fri Feb 12 2016 Dave Airlie <airlied@redhat.com> 3.7.1-4
- rebuild against latest llvm packages
- add BuildRequires llvm-static

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Dave Airlie <airlied@redhat.com> 3.7.1-2
- just accept clang includes moving to /usr/lib64, upstream don't let much else happen

* Thu Jan 28 2016 Dave Airlie <airlied@redhat.com> 3.7.1-1
- initial build in Fedora.

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
