//go:build ignore

#include "vmlinux.h"
#include <bpf/bpf_helpers.h>

char __license[] SEC("license") = "Dual MIT/GPL";

SEC("kprobe/sys_execve")
int hello(void *ctx) {
    bpf_printk("Hello World from eBPF!\n");
    return 0;
}