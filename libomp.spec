%define _prefix /opt/llvm-5.0.1

Name: libomp-5.0.1
Version: 5.0.1
Release:	1.svn319057%{?dist}.alonid
Summary: OpenMP runtime for clang

License: NCSA
URL: http://openmp.llvm.org
Source0:	http://llvm.org/releases/%{version}/29b515e1e6d26b5b0d32d47d28dcdb4b8a11470d.tar.gz

Patch0: 0001-CMake-Make-LIBOMP_HEADERS_INSTALL_PATH-a-cache-varia.patch

BuildRequires: cmake
BuildRequires: elfutils-libelf-devel
BuildRequires: perl
BuildRequires: perl-Data-Dumper
BuildRequires: perl-Encode

Requires: elfutils-libelf

%description
OpenMP runtime for clang.

%package devel
Summary: OpenMP header files

%description devel
OpenMP header files.

%prep
%autosetup -n libomp-29b515e1e6d26b5b0d32d47d28dcdb4b8a11470d -p1

%build
mkdir -p _build
cd _build

%cmake .. \
	-DLIBOMP_INSTALL_ALIASES=OFF \
	-DLIBOMP_HEADERS_INSTALL_PATH:PATH=%{_libdir}/clang/%{version}/include \
%if 0%{?__isa_bits} == 64
	-DLIBOMP_LIBDIR_SUFFIX=64 \
%else
	-DLIBOMP_LIBDIR_SUFFIX= \
%endif

%make_build


%install
cd _build
%make_install


%files
%{_libdir}/libomp.so

%files devel
%{_libdir}/clang/%{version}/include/omp.h

%changelog
* Mon Dec 4 2017 David Wagner <david.wagner@easymile.com> - 5.0.0-1
- Bump to 5.0.0
- Install in /opt/llvm-5.0.0
* Mon May 15 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- Initial version.
