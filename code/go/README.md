# Go eBPF Example

This directory contains a Go example that compiles and attaches an eBPF program to the `execve` syscall using `cilium/ebpf`.

## Files

- `hello.c`
  - The eBPF program written in C.
  - It attaches to the kernel probe for `sys_execve` and prints a message to the kernel trace pipe whenever a new process is executed.
- `main.go`
  - Builds the Go user-space loader.
  - Uses `bpf2go` to generate Go bindings from the eBPF C program.
  - Loads the compiled eBPF object into the kernel, then attaches it to a kprobe.
- `go.mod` / `go.sum`
  - Manage the Go module dependencies.

## How to build

Before running `go generate`, you need a kernel header file named `vmlinux.h` in this folder.

You also need the libbpf development headers so `bpf/bpf_helpers.h` can be found.

On Ubuntu/Debian:

```bash
sudo apt-get install -y bpftool libbpf-dev clang llvm libelf-dev
cd code/go
sudo bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

On Alpine:

```bash
sudo apk add bpftool libbpf-dev clang llvm elfutils-dev
cd code/go
sudo bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

Then build:

```bash
go generate
go build -o hello-ebpf .
```

- `go generate` runs `bpf2go` and generates the Go bindings for the eBPF program.
- `go build` compiles the Go loader into the `hello-ebpf` binary.

## How to run

Run the resulting binary as root:

```bash
sudo ./hello-ebpf
```

Expected output:

```plaintext
2026/07/30 12:00:00 Tracing execve()... Press Ctrl+C to stop.
```

Then in another terminal, run something like:

```bash
ls
whoami
```

You can inspect the kernel trace output with:

```bash
sudo cat /sys/kernel/debug/tracing/trace_pipe
```

You should see lines like:

```plaintext
Hello World from eBPF!
```

## How it works

1. `go:generate` directive in `main.go` calls `bpf2go`.
   - `bpf2go` compiles `hello.c` into eBPF bytecode and generates Go wrappers in a file named `hello_bpf.go`.
2. `main.go` removes the memory lock limit using `rlimit.RemoveMemlock()` so the kernel can allocate eBPF resources.
3. The program loads the generated eBPF object using `loadHelloObjects(&objs, nil)`.
4. It attaches the loaded eBPF program to the `sys_execve` kprobe with `link.Kprobe("sys_execve", objs.Hello, nil)`.
5. Every time `execve()` is called, the eBPF program runs and emits `Hello World from eBPF!` via `bpf_printk()`.

## Notes

- This example requires Linux and a kernel that supports eBPF.
- You must run the resulting binary with root privileges.
- If `bpf2go` is not installed, install it using the `cilium/ebpf` toolchain and ensure Go is available.