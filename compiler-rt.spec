%ifarch s390 s390x
# only limited set of libs available on s390(x) and the existing ones (stats, ubsan) don't provide debuginfo
%global debug_package %{nil}
%endif

%define _prefix /opt/llvm-3.9.1

Name:		compiler-rt-3.9.1
Version:	3.9.1
Release:	3%{?dist}.alonid
Summary:	LLVM "compiler-rt" runtime libraries

License:	NCSA or MIT
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/compiler-rt-3.9.0.src.tar.xz

BuildRequires:	cmake
BuildRequires:	python
BuildRequires:  llvm-%{version}-devel = %{version}
BuildRequires:  llvm-%{version}-static = %{version}
Patch0:         0001-compiler-rt-3.9.1.patch

%description
The compiler-rt project is a part of the LLVM project. It provides
implementation of the low-level target-specific hooks required by
code generation, sanitizer runtimes and profiling library for code
instrumentation, and Blocks C language extension.

%prep
%setup -q -n compiler-rt-3.9.0.src
%patch0 -p1

%build
mkdir -p _build
cd _build
%cmake .. \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DLLVM_CONFIG_PATH:FILEPATH=%{_bindir}/llvm-config-%{__isa_bits} \
	\
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64 \
%else
        -DLLVM_LIBDIR_SUFFIX= \
%endif
	-DCOMPILER_RT_INCLUDE_TESTS:BOOL=OFF # could be on?

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# move sanitizer lists to better place
mkdir -p %{buildroot}%{_libdir}/clang/%{version}
for file in asan_blacklist.txt msan_blacklist.txt dfsan_blacklist.txt cfi_blacklist.txt dfsan_abilist.txt; do
	mv -v %{buildroot}%{_prefix}/${file} %{buildroot}%{_libdir}/clang/%{version}/ || :
done

# move sanitizer libs to better place
mkdir -p %{buildroot}%{_libdir}/clang/%{version}/lib
mv -v %{buildroot}%{_prefix}/lib/linux/libclang_rt* %{buildroot}%{_libdir}/clang/%{version}/lib
mkdir -p %{buildroot}%{_libdir}/clang/%{version}/lib/linux/
pushd %{buildroot}%{_libdir}/clang/%{version}/lib
for i in *.a *.syms *.so; do
	ln -s ../$i linux/$i
done

%check
cd _build
#make check-all

%files
%{_includedir}/*
%{_libdir}/clang/%{version}

%changelog
* Mon Nov 21 2016 Dan Horák <dan[at]danny.cz> - 3.9.0-3
- disable debuginfo on s390(x)

* Wed Nov 02 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-2
- build for new arches.

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-1
- compiler-rt 3.9.0 final release

* Mon May  2 2016 Tom Callaway <spot@fedoraproject.org> 3.8.0-2
- make symlinks to where the linker thinks these libs are

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- compiler-rt 3.8.0 final release

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.2
- compiler-rt 3.8.0rc3

* Thu Feb 18 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-0.1
- compiler-rt 3.8.0rc2

* Fri Feb 05 2016 Dave Airlie <airlied@redhat.com> 3.7.1-3
- fix compiler-rt paths - from rwindz0@gmail.com - #1304605

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
