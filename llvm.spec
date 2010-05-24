Name:           llvm
Version:        2.7
Release:        2%{?dist}
Summary:        The Low Level Virtual Machine

Group:          Development/Languages
License:        NCSA
URL:            http://llvm.org/
Source0:        http://llvm.org/releases/%{version}/llvm-%{version}.tgz
Source1:        http://llvm.org/releases/%{version}/clang-%{version}.tgz
# Data files should be installed with timestamps preserved
Patch0:         llvm-2.6-timestamp.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gcc-c++ >= 3.4
BuildRequires:  groff
BuildRequires:  libtool-ltdl-devel
BuildRequires:  ocaml-ocamldoc
# for DejaGNU test suite
BuildRequires:  dejagnu tcl-devel python
# for doxygen documentation
BuildRequires:  doxygen graphviz

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

%description doc
Documentation for the LLVM compiler infrastructure.


%package -n clang
Summary:        A C language family front-end for LLVM
License:        NCSA
Group:          Development/Languages

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



%prep
%setup -q -n llvm-%{version} -a1 %{?_with_gcc:-a2}
mv clang-%{version} tools/clang

%patch0 -p1 -b .timestamp

# Encoding fix
(cd tools/clang/docs && \
    iconv -f ISO88591 -t UTF8 BlockImplementation.txt \
    -o BlockImplementation.txt)


%build
# Disabling assertions now, rec. by pure and needed for OpenGTL
# TESTFIX no PIC on ix86: http://llvm.org/bugs/show_bug.cgi?id=3801
%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir}/%{name} \
  --datadir=%{_libdir}/%{name} \
  --enable-doxygen \
  --disable-assertions \
  --enable-debug-runtime \
  --enable-jit \
  --enable-shared

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
rm moredocs/*.tar.gz
rm moredocs/ocamldoc/html/*.tar.gz

# and separate the apidoc
mv moredocs/html/doxygen apidoc
mv tools/clang/docs/doxygen/html clang-apidoc

# And prepare Clang documentation
#
mkdir clang-docs
for f in LICENSE.TXT NOTES.txt README.txt TODO.txt; do
  ln tools/clang/$f clang-docs/
done
rm -rf tools/clang/docs/{doxygen*,Makefile*,*.graffle,tools}


#find %{buildroot} -name .dir -print0 | xargs -0r rm -f
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/llvm/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
#chrpath -d %{buildroot}/%{_libexecdir}/clang-cc

# Get rid of erroneously installed example files.
rm %{buildroot}%{_libdir}/%{name}/*LLVMHello.*

# FIXME file this bug
sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}/%{name}",' \
  %{buildroot}%{_bindir}/llvm-config

chmod -x %{buildroot}%{_libdir}/%{name}/*.a

# remove documentation makefiles:
# they require the build directory to work
find examples -name 'Makefile' | xargs -0r rm -f


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CREDITS.TXT LICENSE.TXT README.txt llvm-testlog.txt
%{_bindir}/bugpoint
%{_bindir}/llc
%{_bindir}/lli
%exclude %{_bindir}/llvm-config
%{_bindir}/llvm*
%{_bindir}/opt
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/llvm-%{_arch}.conf
%dir %{_libdir}/llvm
%{_libdir}/llvm/*.so
%exclude %{_mandir}/man1/clang.1.*
%exclude %{_mandir}/man1/llvmg??.1.*
%doc %{_mandir}/man1/*.1.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/llvm-config
%{_includedir}/%{name}
%{_includedir}/%{name}-c
%{_libdir}/%{name}/*.a

%files -n clang
%defattr(-,root,root,-)
%doc clang-docs/* clang-testlog.txt
%{_bindir}/clang*
%{_bindir}/tblgen
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

%files apidoc
%defattr(-,root,root,-)
%doc apidoc/*

%files -n clang-apidoc
%defattr(-,root,root,-)
%doc clang-apidoc/*



%changelog
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
