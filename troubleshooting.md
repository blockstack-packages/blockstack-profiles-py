# Installation Troubleshooting Guide

#### Errors Installing the "cffi" Package

If you see the error shown below on OS X, then there was an issue installing the `cffi` package.

```bash
c/_cffi_backend.c:15:10: fatal error: 'ffi.h' file not found
    #include <ffi.h>
```

To fix this on OS X, try installing *libffi* via brew:

```bash
$ brew install libffi
```

On Debian, you can install libffi by:
```bash
$ sudo apt-get install libffi-dev
```

#### Errors Installing the "cryptography" Package

If you see the error shown below on OS X, then there was an issue installing the `cryptography` package.

```bash
build/temp.macosx-10.10-x86_64-2.7/_openssl.c:423:10: fatal error: 'openssl/e_os2.h' file not found
    #include <openssl/e_os2.h>
```

To fix this issue, try upgrading Xcode Command Line Tools: 

```bash
$ xcode-select --install
```

Then, make sure that openssl is installed and re-link it:

```bash
$ brew install openssl
$ brew link openssl --force
```