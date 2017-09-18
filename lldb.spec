%define _prefix /opt/llvm-5.0.0
%define python_sitearch %{_libdir}/python2.7/site-packages

Name:		lldb-5.0.0
Version:	5.0.0
Release:	2.svn312016%{?dist}.alonid
Summary:	Next generation high-performance debugger

License:	NCSA
URL:		http://lldb.llvm.org/
Source0:	http://llvm.org/releases/%{version}/05c1c5ef75c6a62ff458b1478a52d5d9e4425d84.tar.gz

ExclusiveArch:  %{arm} aarch64 %{ix86} x86_64
# Patch to remove use of private llvm headers
Patch3: 0001-Patch.patch
Patch4: 0001-CentOS-6-cmake-link-fix.patch


%if 0%{?epel} == 6
BuildRequires:	cmake3
BuildRequires:	devtoolset-2-gcc
BuildRequires:	devtoolset-2-binutils
BuildRequires:	devtoolset-2-gcc-c++
BuildRequires:	devtoolset-2-gcc-plugin-devel
BuildRequires:	python27
%else
BuildRequires:	cmake
%endif
BuildRequires:  clang-5.0.0-tools-extra = %{version}
BuildRequires:  llvm-5.0.0-devel = %{version}
BuildRequires:  clang-5.0.0-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  swig
BuildRequires:  llvm-5.0.0-static = %{version}
BuildRequires:  libffi-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
Requires:  clang-5.0.0-libs = %{version}

%description
LLDB is a next generation, high-performance debugger. It is built as a set
of reusable components which highly leverage existing libraries in the
larger LLVM Project, such as the Clang expression parser and LLVM
disassembler.

%package devel
Summary:	Development header files for LLDB
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The package contains header files for the LLDB debugger.

%package -n python-lldb-5.0.0
Summary:	Python module for LLDB
BuildRequires:	python2-devel
Requires:	python2-six

%description -n python-lldb-5.0.0
The package contains the LLDB Python module.

%prep
%setup -q -n lldb-05c1c5ef75c6a62ff458b1478a52d5d9e4425d84

%patch3 -p1
%if 0%{?epel} == 6
%patch4 -p1
%endif

%if 0%{?epel} == 6
%define x__python          %python27__python
%define xpython_sitearch   %python27python_sitearch
%else
%define x__python          %__python
%define xpython_sitearch   %python_sitearch
%endif

%build

export PATH=%{_prefix}/bin:$PATH

mkdir -p _build
cd _build

# Python version detection is broken

%if 0%{?epel} == 6
if [[ "$LD_LIBRARY_PATH" == "" ]] ; then
    export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64
else
    export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64:$LD_LIBRARY_PATH
fi
export PATH=/opt/rh/python27/root/usr/bin:$PATH
if [[ "$PKG_CONFIG_PATH" == "" ]] ; then
    export PKG_CONFIG_PATH=/opt/rh/python27/root/usr/lib64/pkgconfig
else
    export PKG_CONFIG_PATH=/opt/rh/python27/root/usr/lib64/pkgconfig:$PKG_CONFIG_PATH
fi

source /opt/rh/devtoolset-2/enable
%endif

LDFLAGS="%{__global_ldflags} -lpthread -ldl"

CFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=format-security -fno-rtti -fPIC"
CXXFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=format-security -fno-rtti -fPIC"

%if 0%{?epel} == 6
%cmake3 .. \
%else
%cmake .. \
%endif
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_CONFIG:FILEPATH=/usr/bin/llvm-config-%{__isa_bits} \
	\
	-DLLDB_PATH_TO_LLVM_BUILD=%{_prefix} \
	-DLLDB_PATH_TO_CLANG_BUILD=%{_prefix} \
	\
	-DLLDB_DISABLE_CURSES:BOOL=OFF \
	-DLLDB_DISABLE_LIBEDIT:BOOL=ON \
	-DLLDB_DISABLE_PYTHON:BOOL=OFF \
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64 \
%else
        -DLLVM_LIBDIR_SUFFIX= \
%endif
	\
	-DPYTHON_EXECUTABLE:STRING=%{x__python} \
	-DPYTHON_VERSION_MAJOR:STRING=$(%{x__python} -c "import sys; print sys.version_info.major") \
	-DPYTHON_VERSION_MINOR:STRING=$(%{x__python} -c "import sys; print sys.version_info.minor")

make %{?_smp_mflags}

%install

export PATH=%{_prefix}/bin:$PATH

%if 0%{?epel} == 6
if [[ "$LD_LIBRARY_PATH" == "" ]] ; then
    export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64
else
    export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64:$LD_LIBRARY_PATH
fi
export PATH=/opt/rh/python27/root/usr/bin:$PATH
if [[ "$PKG_CONFIG_PATH" == "" ]] ; then
    export PKG_CONFIG_PATH=/opt/rh/python27/root/usr/lib64/pkgconfig
else
    export PKG_CONFIG_PATH=/opt/rh/python27/root/usr/lib64/pkgconfig:$PKG_CONFIG_PATH
fi
source /opt/rh/devtoolset-2/enable
%endif

cd _build
make install DESTDIR=%{buildroot}

# remove static libraries
rm -fv %{buildroot}%{_libdir}/*.a

# python: fix binary libraries location
liblldb=$(basename $(readlink -e %{buildroot}%{_libdir}/liblldb.so))
%if 0%{?epel} != 6
ln -vsf "../../../${liblldb}" %{buildroot}%{xpython_sitearch}/lldb/_lldb.so
%endif
mv -v %{buildroot}%{python_sitearch}/readline.so %{buildroot}%{python_sitearch}/lldb/readline.so

# remove bundled six.py
rm -f %{buildroot}%{python_sitearch}/six.*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/lldb*
%{_bindir}/liblldb-*.so
%{_libdir}/liblldb.so.*
%{_libdir}/*.so

%files devel
%{_includedir}/lldb

%files -n python-lldb-5.0.0
%{python_sitearch}/lldb

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3.9.0-3
- Disable libedit support until upstream fixes it (#1356140)

* Wed Nov  2 2016 Peter Robinson <pbrobinson@fedoraproject.org> 3.9.0-2
- Set upstream supported architectures in an ExclusiveArch

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-1
- lldb 3.9.0
- fixup some issues with MIUtilParse by removing it
- build with -fno-rtti

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- lldb 3.8.0

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.3
- lldb 3.8.0 rc3

* Wed Feb 24 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-0.2
- dynamically link to llvm

* Thu Feb 18 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-0.1
- lldb 3.8.0 rc2

* Sun Feb 14 2016 Dave Airlie <airlied@redhat.com> 3.7.1-3
- rebuild lldb against latest llvm

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
