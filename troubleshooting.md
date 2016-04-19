# Troubleshooting

### Installation

#### Error installing the cffi package

If you see the following error, while *cffi* installs on OS X...

```bash
c/_cffi_backend.c:15:10: fatal error: 'ffi.h' file not found
    #include <ffi.h>
```

...try installing *libffi* via brew:

```bash
$ brew install libffi
```

#### Error installing the cryptography package

If you see the following error, while *cryptography* installs on OS X...

```bash
build/temp.macosx-10.10-x86_64-2.7/_openssl.c:423:10: fatal error: 'openssl/e_os2.h' file not found
    #include <openssl/e_os2.h>
```

1. Try upgrading Xcode Command Line Tools: 

```bash
$ xcode-select --install
```

2. Make sure that openssl is installed:

```bash
$ brew install openssl
```

3. Re-link opensssl:

```bash
$ brew link openssl --force
```