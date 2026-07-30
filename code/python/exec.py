from bcc import BPF

# eBPF program written in C, it runs inside the kernel
program = r"""
int hello(void *ctx) {
    bpf_trace_printk("Hello World from eBPF!\n");
    return 0;
}
"""

# Compile the C code into eBPF bytecode and load it into the kernel
b = BPF(text=program)

# Attach our function to the execve syscall using a kprobe
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")

print("Tracing execve()... Press Ctrl+C to stop.")
b.trace_print()