# eBPF Kernel Example Repository

This repository contains example eBPF programs in Python and Go, plus runtime examples for Falco and Tetragon.

## Ubuntu dependencies

Install BCC, the Python bindings, and LLVM support:

```bash
sudo apt-get update
sudo apt-get install -y bpfcc-tools linux-headers-$(uname -r) python3-bpfcc
sudo apt-get install -y llvm clang
sudo apt-get install -y libbpf-dev libbpf
```

## Alpine dependencies

Install the packages required for BCC, Python, and eBPF development:

```bash
apk update
apk add build-base linux-headers git unzip nano vim elfutils-dev
apk add bcc-tools python3 py3-pip py3-bcc
apk add linux-virt-dev
apk add llvm clang
apk add libbpf-dev libbpf
```

If you need Go support on Alpine:

```bash
apk add go
```

## Examples index

- `code/python/chmod.py` - monitor changes to file permissions on a target file with a BCC kprobe.
- `code/python/delete_file.py` - detect deletion of a target file using a kernel unlink kprobe.
- `code/python/exec.py` - demonstrate attaching an eBPF program to `execve()` with BCC.
- `code/python/ping.py` - monitor outgoing network traffic from the `ping` process.
- `code/python/write_file.py` - detect writes to a target file with a `vfs_write` kprobe.
- `code/go/` - Go example that attaches a kprobe to `sys_execve` and counts how many times it is called.
- `runtime/falco/README.md` - instructions for running Falco in Docker with host mounts.
- `runtime/tetragon/README.md` - instructions for running Tetragon in Docker with a policy file.

## Verify BCC installation

Confirm BCC is available from Python:

```bash
sudo python3 -c "from bcc import BPF; print('BCC installed correctly')"
```

You should see:

```plaintext
BCC installed correctly
```

## Notes

- These dependencies are intended for the examples in this repository.
- For Python examples, run the scripts from `code/python` with `python3`.
- For the Go example, use `go generate` and `go build` inside `code/go`.
