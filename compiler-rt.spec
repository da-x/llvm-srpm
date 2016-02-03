Name:		compiler-rt
Version:	3.7.1
Release:	2%{?dist}
Summary:	LLVM "compiler-rt" runtime libraries

License:	NCSA or MIT
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/%{name}-%{version}.src.tar.xz

BuildRequires:	cmake
BuildRequires:	python
BuildRequires:  llvm-devel = %{version}

%description
The compiler-rt project is a part of the LLVM project. It provides
implementation of the low-level target-specific hooks required by
code generation, sanitizer runtimes and profiling library for code
instrumentation, and Blocks C language extension.

%prep
%setup -q -n %{name}-%{version}.src

%build
mkdir -p _build
cd _build
%cmake .. \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DLLVM_CONFIG_PATH:FILEPATH=%{_bindir}/llvm-config-%{__isa_bits} \
	\
	-DCOMPILER_RT_INCLUDE_TESTS:BOOL=OFF # could be on?

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# move sanitizer lists to better place
mkdir -p %{buildroot}%{_datadir}/%{name}
for file in asan_blacklist.txt dfsan_abilist.txt msan_blacklist.txt; do
	mv -v %{buildroot}%{_prefix}/${file} %{buildroot}%{_datadir}/%{name}/ || :
done

%check
cd _build
#make check-all

%files
%{_includedir}
%{_prefix}/lib/linux
%{_datadir}/%{name}

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
