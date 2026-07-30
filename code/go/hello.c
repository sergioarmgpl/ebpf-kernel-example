//go:build ignore

#include "vmlinux.h"
#include <bpf/bpf_helpers.h>

char __license[] SEC("license") = "Dual MIT/GPL";

SEC("tracepoint/sched/sched_process_exec")
int handle_exec(void *ctx) {
    bpf_printk("Hello World from eBPF!\n");
    return 0;
}