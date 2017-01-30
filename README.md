### RPM packaging for LLVM installed under `/opt/llvm-x.y.z`

This repository contains sources for modified Fedora packages of `LLVM` and assoicated projects. 
The main purpose of the modifications is to allow mutually installable multiple versions of 
`LLVM`, `Clang`, and `compiler-rt` under /opt/llvm-[version].

This work is based on Fedora's packaging.

You can use pre-built binaries linked from below, or you can use [fedpkg](https://pagure.io/fedpkg) under Fedora to generate the SRPMs.

Branches:

 * [llvm-4.0.0 RC (SVN 291918)](https://github.com/da-x/llvm-srpm/tree/llvm-4.0.0), 
   [clang-4.0.0 RC (SVN 293134)](https://github.com/da-x/llvm-srpm/tree/clang-4.0.0),
   [compiler-rt-4.0.0 RC (SVN 292517)](https://github.com/da-x/llvm-srpm/tree/compiler-rt-4.0.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-4.0.0/)**
 * [llvm-3.9.0](https://github.com/da-x/llvm-srpm/tree/llvm-3.9.0), 
   [clang-3.9.0](https://github.com/da-x/llvm-srpm/tree/clang-3.9.0),
   [compiler-rt-3.9.0](https://github.com/da-x/llvm-srpm/tree/compiler-rt-3.9.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.9.0/)**
 * [llvm-3.8.0](https://github.com/da-x/llvm-srpm/tree/llvm-3.8.0), 
   [clang-3.8.0](https://github.com/da-x/llvm-srpm/tree/clang-3.8.0),
   [compiler-rt-3.8.0](https://github.com/da-x/llvm-srpm/tree/compiler-rt-3.8.0),
   **[Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.8.0/)**
 * [llvm-3.7](https://github.com/da-x/llvm-srpm/tree/llvm-3.7)
 * [llvm-3.6](https://github.com/da-x/llvm-srpm/tree/llvm-3.6), [Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.6/)
 * [llvm-3.5](https://github.com/da-x/llvm-srpm/tree/llvm-3.5), [Binaries in Copr](https://copr.fedorainfracloud.org/coprs/alonid/llvm-3.5/)
