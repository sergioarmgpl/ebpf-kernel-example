from bcc import BPF

# File we want to monitor (adjust the name as needed)
TARGET_FILE = "test.txt"

program = r"""
#include <linux/fs.h>

int kprobe__vfs_write(struct pt_regs *ctx, struct file *file, const char __user *buf, size_t count) {
    char fname[64];
    bpf_probe_read_kernel_str(&fname, sizeof(fname), file->f_path.dentry->d_name.name);
    bpf_trace_printk("write to file: %s\n", fname);
    return 0;
}
"""

b = BPF(text=program)

print(f"Listening for writes to '{TARGET_FILE}'... Ctrl+C to exit.")

while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue

    if TARGET_FILE.encode() in msg:
        print(f"[{ts:.6f}] PID {pid} ({task.decode()}) wrote to '{TARGET_FILE}'")
