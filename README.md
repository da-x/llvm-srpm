### RPM packaging for LLVM installed under `/opt/llvm-x.y.z`

This repository contains sources for modified Fedora packages of `LLVM` and associated projects.
The main purpose of the modifications is to allow mutually installable multiple versions of
`LLVM`, `Clang`, `compiler-rt`, and `lldb` under /opt/llvm-[version]. From 5.0.1 onward,
this build also contains the optional `libcxx`, `libcxxabi`, and `libomp` subprojects.

This work is based on Fedora's packaging.

You can use pre-built binaries linked from below, or you can use [fedpkg](https://pagure.io/fedpkg) under Fedora to generate the SRPMs.

Branches:

 * [llvm-5.0.1 (SVN 319952)](https://github.com/da-x/llvm-srpm/tree/llvm-5.0.1),
   [clang-5.0.1 (SVN 319847)](https://github.com/da-x/llvm-srpm/tree/clang-5.0.1),
   [compiler-rt-5.0.1 (SVN 311736)](https://github.com/da-x/llvm-srpm/tree/compiler-rt-5.0.1),
   [lldb-5.0.1 (SVN 319035)](https://github.com/da-x/llvm-srpm/tree/lldb-5.0.1),
   [libomp-5.0.1 (SVN 319057)](https://github.com/da-x/llvm-srpm/tree/libomp-5.0.1),
   [libcxx-5.0.1 (SVN 318837)](https://github.com/da-x/llvm-srpm/tree/libcxx-5.0.1),
   [libcxxabi-5.0.1 (SVN 308470)](https://github.com/da-x/llvm-srpm/tree/libcxxabi-5.0.1),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-5.0.1/)**
 * [llvm-5.0.0 (SVN 312333)](https://github.com/da-x/llvm-srpm/tree/llvm-5.0.0),
   [clang-5.0.0 (SVN 312293)](https://github.com/da-x/llvm-srpm/tree/clang-5.0.0),
   [compiler-rt-5.0.0 (SVN 311736)](https://github.com/da-x/llvm-srpm/tree/compiler-rt-5.0.0),
   [lldb-5.0.0 (SVN 312016)](https://github.com/da-x/llvm-srpm/tree/lldb-5.0.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-5.0.0/)**
 * [llvm-4.0.0 (SVN 297204)](https://github.com/da-x/llvm-srpm/tree/llvm-4.0.0),
   [clang-4.0.0 (SVN 293134)](https://github.com/da-x/llvm-srpm/tree/clang-4.0.0),
   [compiler-rt-4.0.0 (SVN 292518)](https://github.com/da-x/llvm-srpm/tree/compiler-rt-4.0.0),
   [lldb-4.0.0 (SVN 291842)](https://github.com/da-x/llvm-srpm/tree/lldb-4.0.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-4.0.0/)**
 * [llvm-3.9.1](https://github.com/da-x/llvm-srpm/tree/llvm-3.9.1),
   [clang-3.9.1](https://github.com/da-x/llvm-srpm/tree/clang-3.9.1),
   [compiler-rt-3.9.1](https://github.com/da-x/llvm-srpm/tree/compiler-rt-3.9.1),
   [lldb-3.9.1](https://github.com/da-x/llvm-srpm/tree/lldb-3.9.1),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.9.1/)**
 * [llvm-3.8.0](https://github.com/da-x/llvm-srpm/tree/llvm-3.8.0),
   [clang-3.8.0](https://github.com/da-x/llvm-srpm/tree/clang-3.8.0),
   [compiler-rt-3.8.0](https://github.com/da-x/llvm-srpm/tree/compiler-rt-3.8.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.8.0/)**
 * [llvm-3.7](https://github.com/da-x/llvm-srpm/tree/llvm-3.7)
 * [llvm-3.6](https://github.com/da-x/llvm-srpm/tree/llvm-3.6), [Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.6/)
 * [llvm-3.5](https://github.com/da-x/llvm-srpm/tree/llvm-3.5), [Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.5/)
