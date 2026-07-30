## How to install BCC and its dependencies on Ubuntu

**1.** Inside the Killercoda Ubuntu playground, update the package index and install the BCC tools package, which ships the Python bindings, the `bpfcc-tools`, and the required kernel headers:

```shell
sudo apt-get update
sudo apt-get install -y bpfcc-tools linux-headers-$(uname -r) python3-bpfcc
sudo apt-get install llvm clang
```

## How to install BCC and its dependencies on Alpine
```shell
apk update 
apk add build-base linux-headers git unzip nano vim elfutils-dev
apk add bcc-tools python3 py3-pip py3-bcc
apk add linux-virt-dev
apk add llvm clang
```

If you need Go for building or running Go-based tools, install it with:

```shell
apk add go
```



**2.** Verify that BCC is installed correctly by importing it from Python:

```shell
sudo python3 -c "from bcc import BPF; print('BCC installed correctly')"
```


You should see:

```plaintext
BCC installed correctly
```

BCC takes care of compiling the C code you write into eBPF bytecode using LLVM, and of loading that bytecode into the kernel through the `bpf()` system call, so you don't need a separate cross-compilation toolchain to get started.

To run the examples using BCC with python follow the next steps:

1. Change to the code directory
```
cd code/python
```
2. Run the example using Python
```
python3 EXAMPLE.py
```