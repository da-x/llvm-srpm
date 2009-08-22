# Build options:
#
# --with doxygen
#   The doxygen docs are HUGE, so they are not built by default.
#
# --with gcc
#   The llvm-gcc package doesn't currently build.

%define lgcc_version 4.2

# LLVM object files don't contain build IDs.  I don't know why yet.
# Suppress their generation for now.

%define debug_package %{nil}

Name:           llvm
Version:        2.5
Release:        4%{?dist}
Summary:        The Low Level Virtual Machine

Group:          Development/Languages
License:        NCSA
URL:            http://llvm.org/
Source0:        http://llvm.org/releases/%{version}/llvm-%{version}.tar.gz
%if %{?_with_gcc:1}%{!?_with_gcc:0}
Source1:        http://llvm.org/releases/%{version}/llvm-gcc-%{lgcc_version}-%{version}.source.tar.gz
%endif
Patch0:         llvm-2.1-fix-sed.patch
Patch1:         llvm-2.4-fix-ocaml.patch
# http://llvm.org/bugs/show_bug.cgi?id=3726
Patch2:         llvm-2.5-gcc44.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gcc-c++ >= 3.4
BuildRequires:  groff
BuildRequires:  libtool-ltdl-devel
BuildRequires:  ocaml-ocamldoc
%if %{?_with_doxygen:1}%{!?_with_doxygen:0}
BuildRequires:  doxygen graphviz
%endif

# LLVM is not supported on PPC64
# http://llvm.org/bugs/show_bug.cgi?id=3729
ExcludeArch:    ppc64

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages.  The compiler infrastructure includes
mirror sets of programming tools as well as libraries with equivalent
functionality.

%if %{?_with_gcc:1}%{!?_with_gcc:0}
It currently supports compilation of C and C++ programs, using front
ends derived from GCC %{lgcc_version}.
%endif


%package devel
Summary:        Libraries and header files for LLVM
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel >= 3.4


%description devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.


%package doc
Summary:        Documentation for LLVM
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.


%if %{?_with_gcc:1}%{!?_with_gcc:0}

%package gcc
Summary:        C compiler for LLVM
License:        GPL+
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}


%description gcc
C compiler for LLVM.


%package gcc-c++
Summary:        C++ compiler for LLVM
License:        GPL+
Group:          Development/Languages
Requires:       %{name}-gcc = %{version}-%{release}


%description gcc-c++
C++ compiler for LLVM.

%endif


%if %{?_with_doxygen:1}%{!?_with_doxygen:0}
%package apidoc
Summary:        API documentation for LLVM
Group:          Development/Languages
Requires:       %{name}-docs = %{version}-%{release}


%description apidoc
API documentation for the LLVM compiler infrastructure.
%endif


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

%description    ocaml-devel
The %{name}-ocaml-devel package contains libraries and signature files
for developing applications that use %{name}-ocaml.


%prep
%setup -q -n llvm-%{version} %{?_with_gcc:-a1}

%patch0 -p1 -b .fix-sed
%patch1 -p1 -b .fix-ocaml
%patch2 -p1 -b .gcc44

%build
# Note: --enable-pic can be turned off when 2.6 comes out
#       and up to 2.5, unsafe on 32-bit archs (in our case,
#       anything but x86_64)
%configure \
  --libdir=%{_libdir}/%{name} \
  --datadir=%{_datadir}/%{name}-%{version} \
  --disable-static \
  --enable-assertions \
  --enable-debug-runtime \
  --enable-jit \
  --enable-optimized \
%ifarch x86_64
  --enable-pic
%endif
#   --enable-targets=host-only \

make %{_smp_mflags} OPTIMIZE_OPTION='%{optflags}'
# tools-only VERBOSE=1 OmitFramePointer='' REQUIRES_EH=1 \
#  OPTIMIZE_OPTION='%{optflags}'

%if %{?_with_gcc:1}%{!?_with_gcc:0}
# Build llvm-gcc.

export PATH=%{_builddir}/%{?buildsubdir}/Release/bin:$PATH

mkdir llvm-gcc%{lgcc_version}-%{version}.source/build
cd llvm-gcc%{lgcc_version}-%{version}.source/build

../configure \
  --host=%{_host} \
  --build=%{_build} \
  --target=%{_target_platform} \
  --prefix=%{_libdir}/llvm-gcc \
  --libdir=%{_libdir}/llvm-gcc/%{_lib} \
  --enable-threads \
  --disable-nls \
%ifarch x86_64
  --disable-multilib \
  --disable-shared \
%endif
  --enable-languages=c,c++ \
  --enable-llvm=%{_builddir}/%{?buildsubdir} \
  --program-prefix=llvm-
make %{_smp_mflags} LLVM_VERSION_INFO=%{version}
%endif

%install
rm -rf %{buildroot}
chmod -x examples/Makefile
# OVERRIDE_libdir used by our patched Makefile.ocaml:
# see http://llvm.org/bugs/show_bug.cgi?id=3153
make install DESTDIR=%{buildroot} \
     PROJ_libdir=%{buildroot}/%{_libdir}/%{name} \
     OVERRIDE_libdir=%{_libdir}/%{name}/%{name} \
     PROJ_docsdir=`pwd`/moredocs

#make install \
#  PROJ_prefix=%{buildroot}/%{_prefix} \
#  PROJ_bindir=%{buildroot}/%{_bindir} \
#  PROJ_libdir=%{buildroot}/%{_libdir}/%{name} \
#  PROJ_datadir=%{buildroot}/%{_datadir} \
#  PROJ_docsdir=%{buildroot}/%{_docdir}/%{name}-%{version} \
#  PROJ_etcdir=%{buildroot}/%{_datadir}/%{name}-%{version} \
#  PROJ_includedir=%{buildroot}/%{_includedir} \
#  PROJ_infodir=%{buildroot}/%{_infodir} \
#  PROJ_mandir=%{buildroot}/%{_mandir}
find %{buildroot} -name .dir -print0 | xargs -0r rm -f
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d

# Get rid of erroneously installed example files.
rm %{buildroot}%{_libdir}/%{name}/LLVMHello.*

# And OCaml .o files
rm %{buildroot}%{_libdir}/ocaml/*.o

# Use relative links for ocaml's libLLVM*.a
#(cd %{buildroot}%{_libdir}/ocaml && for i in libLLVM*.a; do
#    ln -sf %{_libdir}/llvm/$i $i;
# done)

# Remove deprecated tools.
rm %{buildroot}%{_bindir}/gcc{as,ld}

sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}/%{name}",' \
  %{buildroot}%{_bindir}/llvm-config

chmod -x %{buildroot}%{_libdir}/%{name}/*.[oa]

# remove documentation makefiles:
# they require the build directory to work
find examples -name 'Makefile'

%if %{?_with_gcc:1}%{!?_with_gcc:0}
# Install llvm-gcc.

make -C llvm-gcc%{lgcc_version}-%{version}.source/build install DESTDIR=%{buildroot}
cd %{buildroot}%{_libdir}/llvm-gcc/%{_lib}
find . -name '*.la' -print0 | xargs -0r rm
find . -name '*.a' -exec %{buildroot}%{_bindir}/llvm-ranlib {} \;
cd ../bin
ln llvm-c++ llvm-gcc llvm-g++ %{buildroot}%{_bindir}
rm llvm-cpp llvm-gccbug llvm-gcov %{_target_platform}-gcc*
cd ..
mv man/man1/llvm-gcc.1 man/man1/llvm-g++.1 %{buildroot}%{_mandir}/man1
rm -r info man %{_lib}/libiberty.a
rm -r libexec/gcc/%{_target_platform}/%{lgcc_version}/install-tools
rm -r %{_lib}/gcc/%{_target_platform}/%{lgcc_version}/install-tools
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CREDITS.TXT LICENSE.TXT README.txt
%exclude %{_bindir}/llvm-config
%{_bindir}/bugpoint
%{_bindir}/llc
%{_bindir}/lli
%{_bindir}/llvm*
%{_bindir}/opt
%doc %{_mandir}/man1/*.1.gz

%if %{?_with_doxygen:1}%{!?_with_doxygen:0}
%exclude %{_bindir}/llvm-[cg]++
%exclude %{_bindir}/llvm-gcc
%exclude %{_mandir}/man1/llvm-[cg]++.*
%exclude %{_mandir}/man1/llvm-gcc.*
%endif


%files devel
%defattr(-,root,root,-)
%{_bindir}/llvm-config
%{_includedir}/%{name}
%{_includedir}/%{name}-c
%{_libdir}/%{name}


%files ocaml
%defattr(-,root,root,-)
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/*.cmi

%files ocaml-devel
%defattr(-,root,root,-)
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmx*
%{_libdir}/ocaml/*.mli

%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,css} docs/img examples moredocs/*


%if %{?_with_doxygen:1}%{!?_with_doxygen:0}
%files apidoc
%defattr(-,root,root,-)
%doc docs/doxygen
%endif


%if %{?_with_gcc:1}%{!?_with_gcc:0}
%files gcc
%defattr(-,root,root,-)
%{_bindir}/llvm-gcc
%dir %{_libdir}/llvm-gcc
%dir %{_libdir}/llvm-gcc/bin
%dir %{_libdir}/llvm-gcc/include
%dir %{_libdir}/llvm-gcc/%{_lib}
%dir %{_libdir}/llvm-gcc/libexec
%dir %{_libdir}/llvm-gcc/libexec/gcc
%dir %{_libdir}/llvm-gcc/libexec/gcc/%{_target_platform}/%{lgcc_version}
%{_libdir}/llvm-gcc/%{_lib}/gcc
%{_libdir}/llvm-gcc/%{_lib}/libmudflap*.a
%{_libdir}/llvm-gcc/bin/%{_target_platform}-llvm-gcc
%{_libdir}/llvm-gcc/bin/llvm-gcc
%{_libdir}/llvm-gcc/include/mf-runtime.h
%{_libdir}/llvm-gcc/libexec/gcc/%{_target_platform}/%{lgcc_version}/cc1
%{_libdir}/llvm-gcc/libexec/gcc/%{_target_platform}/%{lgcc_version}/collect2
%doc %{_mandir}/man1/llvm-gcc.*


%files gcc-c++
%defattr(-,root,root,-)
%{_bindir}/llvm-[cg]++
%{_libdir}/llvm-gcc/%{_lib}/lib*++.a
%{_libdir}/llvm-gcc/bin/%{_target_platform}-llvm-[cg]++
%{_libdir}/llvm-gcc/bin/llvm-[cg]++
%{_libdir}/llvm-gcc/include/c++
%{_libdir}/llvm-gcc/libexec/gcc/%{_target_platform}/%{lgcc_version}/cc1plus
%doc %{_mandir}/man1/llvm-g++.*
%endif


%changelog
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
