Name:		lldb
Version:	3.8.0
Release:	1%{?dist}
Summary:	Next generation high-performance debugger

License:	NCSA
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.src.tar.xz

# hack patch from upstream review systems to fix out of tree builds.
Patch0: D15067.id41365.diff

BuildRequires:	cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  clang-devel = %{version}
BuildRequires:	libedit-devel
BuildRequires:  swig
BuildRequires:  llvm-static = %{version}
BuildRequires:  libffi-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel

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

%package -n python-lldb
Summary:	Python module for LLDB
BuildRequires:	python2-devel
Requires:	python2-six

%description -n python-lldb
The package contains the LLDB Python module.

%prep
%setup -q -n %{name}-%{version}.src

%patch0 -p1 -b .dave
%build
mkdir -p _build
cd _build

# Python version detection is broken

LDFLAGS="%{__global_ldflags} -lpthread -ldl"

CFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=format-security"
CXXFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=format-security"

%cmake .. \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_CONFIG:FILEPATH=/usr/bin/llvm-config-%{__isa_bits} \
	\
	-DLLDB_PATH_TO_LLVM_BUILD=%{_prefix} \
	-DLLDB_PATH_TO_CLANG_BUILD=%{_prefix} \
	\
	-DLLDB_DISABLE_CURSES:BOOL=OFF \
	-DLLDB_DISABLE_LIBEDIT:BOOL=OFF \
	-DLLDB_DISABLE_PYTHON:BOOL=OFF \
	\
	-DPYTHON_EXECUTABLE:STRING=%{__python} \
	-DPYTHON_VERSION_MAJOR:STRING=$(%{__python} -c "import sys; print sys.version_info.major") \
	-DPYTHON_VERSION_MINOR:STRING=$(%{__python} -c "import sys; print sys.version_info.minor")

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# remove static libraries
rm -fv %{buildroot}%{_libdir}/*.a

# python: fix binary libraries location
liblldb=$(basename $(readlink -e %{buildroot}%{_libdir}/liblldb.so))
ln -vsf "../../../${liblldb}" %{buildroot}%{python_sitearch}/lldb/_lldb.so
mv -v %{buildroot}%{python_sitearch}/readline.so %{buildroot}%{python_sitearch}/lldb/readline.so

# remove bundled six.py
rm -f %{buildroot}%{python_sitearch}/six.*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/lldb*
%{_libdir}/liblldb.so.*

%files devel
%{_includedir}/lldb
%{_libdir}/*.so

%files -n python-lldb
%{python_sitearch}/lldb

%changelog
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
