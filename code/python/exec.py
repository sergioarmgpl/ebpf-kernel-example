from bcc import BPF
BPF(text='int kprobe__sys_clone(void *ctx) { bpf_trace_printk("Hello, World!\\n"); return 0; }').trace_print()


# Captures the output of the BPF program and prints it to the console. The BPF program is attached to the `sys_clone` kernel function, and whenever a process is cloned, it will print "Hello, World!" to the trace pipe.
