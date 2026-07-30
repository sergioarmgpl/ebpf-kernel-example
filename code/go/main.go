package main

import (
    "log"
    "os"
    "os/signal"

    "github.com/cilium/ebpf/link"
    "github.com/cilium/ebpf/rlimit"
)

//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -target amd64 hello hello.c

func main() {
    stopper := make(chan os.Signal, 1)
    signal.Notify(stopper, os.Interrupt)

    // Allow the current process to lock memory for eBPF resources.
    if err := rlimit.RemoveMemlock(); err != nil {
        log.Fatal(err)
    }

    // Load the compiled eBPF program into the kernel.
    objs := helloObjects{}
    if err := loadHelloObjects(&objs, nil); err != nil {
        log.Fatalf("loading objects: %v", err)
    }
    defer objs.Close()

    // Attach the program to the sched_process_exec tracepoint.
    tp, err := link.Tracepoint("sched", "sched_process_exec", objs.Hello, nil)
    if err != nil {
        log.Fatalf("opening tracepoint: %s", err)
    }
    defer tp.Close()

    log.Println("Tracing execve()... Press Ctrl+C to stop.")
    <-stopper
    log.Println("Detaching kprobe, exiting.")
}