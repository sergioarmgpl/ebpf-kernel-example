# Go eBPF Example

This directory contains a Go example that uses a kprobe to count how many times the kernel function `sys_execve` is entered.

## What it does

The example compiles an eBPF program from `kprobe.c` and loads it with a Go loader in `main.go`.

- The eBPF program increments a counter in a BPF map each time `sys_execve` is called.
- The Go program attaches that eBPF code to the kernel function entry point using `link.Kprobe`.
- Every second, the Go program reads the map and prints how many times `sys_execve` has been invoked.

This effectively provides a live count of process execution events on the host.

## Files

- `kprobe.c`
  - The eBPF C program.
  - It contains the probe attached to `sys_execve` and the map used to count events.
- `main.go`
  - The Go loader and user-space control loop.
  - It runs `go generate`, loads the compiled BPF object, attaches the kprobe, and polls the map.
- `go.mod` / `go.sum`
  - Go module dependency files.

## How to build and run

From this directory:

```bash
go generate
go build -o kprobe-example .
```

Then run the binary as root:

```bash
sudo ./kprobe-example
```

You should see output like:

```plaintext
Waiting for events..
```

And then, once `execve` events occur, lines such as:

```plaintext
sys_execve called 1 times
sys_execve called 2 times
```

## How to test it

In another terminal, run a command such as:

```bash
ls
whoami
```

The Go program should increase the count each time a new program starts.

## How it works

1. `main.go` calls `rlimit.RemoveMemlock()` so the process can lock memory for BPF resources.
2. It loads the generated BPF objects with `loadBpfObjects`.
3. It attaches the eBPF program to `sys_execve` using `link.Kprobe(fn, objs.KprobeExecve, nil)`.
4. The eBPF program increments a counter in `KprobeMap` every time the probe fires.
5. The Go loop reads that counter once per second and logs the total.

## Notes

- You must run the binary with root privileges.
- The `go:generate` directive in `main.go` uses `go tool bpf2go -tags linux bpf kprobe.c -- -I../headers` to generate Go bindings.
- Ensure your environment has the required eBPF toolchain, Go, and kernel headers available.
