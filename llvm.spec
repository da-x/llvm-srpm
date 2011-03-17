# Build options:
#
# --with doxygen
#   The doxygen docs are HUGE, so they are not built by default.

%ifarch s390 s390x sparc64
  # No ocaml on these arches
  %bcond_with ocaml
%else
  %bcond_without ocaml
%endif

%global prerel rc1
%global downloadurl http://llvm.org/%{?prerel:pre-}releases/%{version}

Name:           llvm
Version:        2.9
Release:        0.2.%{prerel}%{?dist}
Summary:        The Low Level Virtual Machine

Group:          Development/Languages
License:        NCSA
URL:            http://llvm.org/
Source0:        %{downloadurl}/llvm-%{version}%{?prerel}.src.tar.gz
Source1:        %{downloadurl}/clang-%{version}%{?prerel}.src.tar.gz
# Data files should be installed with timestamps preserved
Patch0:         llvm-2.6-timestamp.patch

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gcc-c++ >= 3.4
BuildRequires:  groff
BuildRequires:  libtool-ltdl-devel
%if %{with ocaml}
BuildRequires:  ocaml-ocamldoc
%endif
# for DejaGNU test suite
BuildRequires:  dejagnu tcl-devel python
# for doxygen documentation
%if 0%{?_with_doxygen}
BuildRequires:  doxygen graphviz
%endif
Requires:       llvm-libs = %{version}-%{release}

# LLVM is not supported on PPC64
# http://llvm.org/bugs/show_bug.cgi?id=3729
ExcludeArch:    ppc64

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages.  The compiler infrastructure includes
mirror sets of programming tools as well as libraries with equivalent
functionality.


%package devel
Summary:        Libraries and header files for LLVM
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel >= 3.4
Provides:       llvm-static = %{version}-%{release}


%description devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.


%package doc
Summary:        Documentation for LLVM
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
# might seem redundant, but needed to kill off the old arch-ed -doc
# subpackage
Obsoletes:      %{name}-doc < %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.


%package libs
Summary:        LLVM shared libraries
Group:          System Environment/Libraries

%description libs
Shared libraries for the LLVM compiler infrastructure.


%package -n clang
Summary:        A C language family front-end for LLVM
License:        NCSA
Group:          Development/Languages
Requires:       llvm = %{version}-%{release}
# clang requires gcc; clang++ gcc-c++
Requires:       gcc-c++

%description -n clang
clang: noun
    1. A loud, resonant, metallic sound.
    2. The strident call of a crane or goose.
    3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extensible.


%package -n clang-devel
Summary:        Header files for clang
Group:          Development/Languages
Requires:       clang = %{version}-%{release}

%description -n clang-devel
This package contains header files for the Clang compiler.


%package -n clang-analyzer
Summary:        A source code analysis framework
License:        NCSA
Group:          Development/Languages
Requires:       clang = %{version}-%{release}
# not picked up automatically since files are currently not instaled
# in standard Python hierarchies yet
Requires:       python

%description -n clang-analyzer
The Clang Static Analyzer consists of both a source code analysis
framework and a standalone tool that finds bugs in C and Objective-C
programs. The standalone tool is invoked from the command-line, and is
intended to run in tandem with a build of a project or code base.


%package -n clang-doc
Summary:        Documentation for Clang
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description -n clang-doc
Documentation for the Clang compiler front-end.


%if 0%{?_with_doxygen}
%package apidoc
Summary:        API documentation for LLVM
Group:          Development/Languages
BuildArch:      noarch
Requires:       %{name}-doc = %{version}-%{release}


%description apidoc
API documentation for the LLVM compiler infrastructure.


%package -n clang-apidoc
Summary:        API documentation for Clang
Group:          Development/Languages
BuildArch:      noarch
Requires:       clang-doc = %{version}-%{release}


%description -n clang-apidoc
API documentation for the Clang compiler.
%endif


%if %{with ocaml}
%package        ocaml
Summary:        OCaml binding for LLVM
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-runtime

%description    ocaml
OCaml binding for LLVM.


%package        ocaml-devel
Summary:        Development files for %{name}-ocaml
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-ocaml = %{version}-%{release}
Requires:       ocaml

%description    ocaml-devel
The %{name}-ocaml-devel package contains libraries and signature files
for developing applications that use %{name}-ocaml.


%package ocaml-doc
Summary:        Documentation for LLVM's OCaml binding
Group:          Documentation
BuildArch:      noarch
Requires:       %{name}-ocaml = %{version}-%{release}

%description ocaml-doc
HTML documentation for LLVM's OCaml binding.
%endif


%prep
%setup -q -n llvm-%{version}%{?prerel} -a1 %{?_with_gcc:-a2}
mv clang-%{version}%{?prerel} tools/clang

%patch0 -p1 -b .timestamp
pushd tools/clang
popd

# Encoding fix
#(cd tools/clang/docs && \
#    iconv -f ISO88591 -t UTF8 BlockImplementation.txt \
#    -o BlockImplementation.txt)


%build
# Disabling assertions now, rec. by pure and needed for OpenGTL
# TESTFIX no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3801
%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir}/%{name} \
  --datadir=%{_libdir}/%{name} \
%if 0%{?_with_doxygen}
  --enable-doxygen \
%endif
  --disable-assertions \
  --enable-debug-runtime \
  --enable-jit \
  --enable-shared \
  --with-c-include-dirs=%{_includedir}:$(find %{_prefix}/lib/gcc/*/* \
      -maxdepth 0 -type d)/include \
  --with-cxx-include-root=$(find %{_includedir}/c++/* -maxdepth 0 -type d) \
  --with-cxx-include-arch=%{_arch}-%{_vendor}-%{_os} \
  --with-cxx-include-32bit-dir=32

# FIXME file this
# configure does not properly specify libdir
sed -i 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_lib}/%{name}|g' Makefile.config

make %{_smp_mflags} \
%ifarch ppc
  OPTIMIZE_OPTION="%{optflags} -fno-var-tracking-assignments"
%else
  OPTIMIZE_OPTION="%{optflags}"
%endif


%check
# no current unexpected failures. Use || true if they recur to force ignore
make check 2>&1 | tee llvm-testlog.txt
(cd tools/clang && make test 2>&1) | tee clang-testlog.txt


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} \
     PROJ_docsdir=/moredocs

# Create ld.so.conf.d entry
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/llvm-%{_arch}.conf << EOF
%{_libdir}/llvm
EOF

# Static analyzer not installed by default:
# http://clang-analyzer.llvm.org/installation#OtherPlatforms
mkdir -p %{buildroot}%{_libdir}/clang-analyzer
# create launchers
for f in scan-{build,view}; do
  ln -s %{_libdir}/clang-analyzer/$f/$f %{buildroot}%{_bindir}/$f
done

(cd tools/clang/tools && cp -pr scan-{build,view} \
 %{buildroot}%{_libdir}/clang-analyzer/)


# Move documentation back to build directory
# 
mv %{buildroot}/moredocs .
rm -f moredocs/*.tar.gz
rm -f moredocs/ocamldoc/html/*.tar.gz

# and separate the apidoc
%if 0%{?_with_doxygen}
mv moredocs/html/doxygen apidoc
mv tools/clang/docs/doxygen/html clang-apidoc
%endif

# And prepare Clang documentation
#
mkdir clang-docs
for f in LICENSE.TXT NOTES.txt README.txt TODO.txt; do
  ln tools/clang/$f clang-docs/
done
rm -rf tools/clang/docs/{doxygen*,Makefile*,*.graffle,tools}


#find %%{buildroot} -name .dir -print0 | xargs -0r rm -f
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/llvm/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
#chrpath -d %%{buildroot}/%%{_libexecdir}/clang-cc

# Get rid of erroneously installed example files.
rm %{buildroot}%{_libdir}/%{name}/*LLVMHello.*

# FIXME file this bug
sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}/%{name}",' \
  %{buildroot}%{_bindir}/llvm-config

chmod -x %{buildroot}%{_libdir}/%{name}/*.a

# remove documentation makefiles:
# they require the build directory to work
find examples -name 'Makefile' | xargs -0r rm -f


%post libs -p /sbin/ldconfig
%post -n clang -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig
%postun -n clang -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CREDITS.TXT LICENSE.TXT README.txt
%{_bindir}/bugpoint
%{_bindir}/llc
%{_bindir}/lli
%exclude %{_bindir}/llvm-config
%{_bindir}/llvm*
%{_bindir}/macho-dump
%{_bindir}/opt
%exclude %{_mandir}/man1/clang.1.*
%exclude %{_mandir}/man1/llvmg??.1.*
%doc %{_mandir}/man1/*.1.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/llvm-config
%{_includedir}/%{name}
%{_includedir}/%{name}-c
%{_libdir}/%{name}/*.a

%files libs
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/llvm-%{_arch}.conf
%dir %{_libdir}/%{name}
%exclude %{_libdir}/%{name}/libclang.so
%{_libdir}/%{name}/*.so

%files -n clang
%defattr(-,root,root,-)
%doc clang-docs/*
%{_bindir}/clang*
#%{_bindir}/c-index-test
%{_bindir}/tblgen
%{_libdir}/%{name}/libclang.so
%{_prefix}/lib/clang
%doc %{_mandir}/man1/clang.1.*

%files -n clang-devel
%defattr(-,root,root,-)
%{_includedir}/clang
%{_includedir}/clang-c

%files -n clang-analyzer
%defattr(-,root,root,-)
%{_bindir}/scan-build
%{_bindir}/scan-view
%{_libdir}/clang-analyzer

%files -n clang-doc
%defattr(-,root,root,-)
%doc tools/clang/docs/*

%files doc
%defattr(-,root,root,-)
%doc examples moredocs/html

%if %{with ocaml}
%files ocaml
%defattr(-,root,root,-)
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/*.cmi

%files ocaml-devel
%defattr(-,root,root,-)
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmx*
%{_libdir}/ocaml/*.mli

%files ocaml-doc
%defattr(-,root,root,-)
%doc moredocs/ocamldoc/html/*
%endif

%if 0%{?_with_doxygen}
%files apidoc
%defattr(-,root,root,-)
%doc apidoc/*

%files -n clang-apidoc
%defattr(-,root,root,-)
%doc clang-apidoc/*
%endif


%changelog
* Thu Mar 18 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-0.2.rc1
- Split shared libraries into separate subpackage
- Don't include test logs; breaks multilib (# 666195)
- clang++: also search for platform-specific include files (# 680644)

* Thu Mar 10 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-0.1.rc1
- Update to 2.9rc1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Richard W.M. Jones <rjones@redhat.com> - 2.8-6
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Sat Nov 27 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-5
- clang now requires gcc-c++ for linking and headers (bug #654560)

* Fri Nov 12 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-4
- Backport support for C++0x (# 648990)

* Fri Oct 15 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-3
- Re-add omitted %%{_includedir}

* Thu Oct 14 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-2
- Add correct C include directory at compile time (# 641500)

* Tue Oct 12 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-1
- Update to 2.8 release

* Wed Sep 29 2010 jkeating - 2.7-10
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-9
- Dynamically determine C++ include path at compile time (# 630474)
- Remove unneeded BuildRoot field and clean section

* Wed Sep 15 2010 Dennis Gilmore <dennis@ausil.us> - 2.7-8
- disable ocaml support on sparc64

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.7-7
- recompiling .py files against Python 2.7 (rhbz#623332)

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 2.7-6
- conditionalize ocaml support

* Mon Jun  7 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-5
- Make the new noarch -doc obsoletes older (arched) subpackages

* Sat Jun  5 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-4
- Add F-12/x86_64 and F-13 C++ header paths

* Wed May 26 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-3
- Revert to disabling apidoc by default

* Mon May 24 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-2
- Exclude llm-gcc manpages
- Turn on apidoc generation
- Build with srcdir=objdir, otherwise clang doxygen build fails

* Sun May  2 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-1
- Update to final 2.7 release

* Sun Mar 28 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-0.1.pre1
- Update to first 2.7 pre-release

* Fri Sep 18 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.6.pre2
- Update to 2.6 pre-release2
- -devel subpackage now virtually provides -static

* Wed Sep  9 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.5.pre1
- Disable var tracking assignments on PPC

* Wed Sep  9 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.4.pre1
- Don't adjust clang include dir; files there are noarch (bz#521893)
- Enable clang unit tests
- clang and clang-analyzer renamed; no longer depend on llvm at runtime

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.3.pre1
- Package Clang's static analyzer tools

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.2.pre1
- PIC is now enabled by default; explicitly disable on %%{ix86}

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.1.pre1
- First 2.6 prerelease
- Enable Clang front-end
- Enable debuginfo generation

* Sat Sep  5 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-6
- Disable assertions (needed by OpenGTL, bz#521261)
- Align spec file with upstream build instructions
- Enable unit tests

* Sat Aug 22 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-5
- Only disable PIC on %%ix86; ppc actually needs it

* Sat Aug 22 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-4
- Disable use of position-independent code on 32-bit platforms
  (buggy in LLVM <= 2.5)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar  4 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-2
- Remove build scripts; they require the build directory to work

* Wed Mar  4 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-1
- Update to 2.5
- Package build scripts (bug #457881)

* Tue Dec  2 2008 Michel Salim <salimma@fedoraproject.org> - 2.4-2
- Patched build process for the OCaml binding

* Tue Dec  2 2008 Michel Salim <salimma@fedoraproject.org> - 2.4-1
- Update to 2.4
- Package Ocaml binding

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.3-2
- Add dependency on groff

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.3-1
- LLVM 2.3

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-4
- fix license tags

* Wed Mar  5 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.2-3
- Fix compilation problems with gcc 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.1-2
- Fix review comments

* Sun Jan 20 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.1-1
- Initial version
