from bcc import BPF

TARGET_FILE = "test.txt"

program = r"""
#include <linux/fs.h>

int kprobe__security_inode_unlink(struct pt_regs *ctx, struct inode *dir, struct dentry *dentry) {
    char fname[64];
    bpf_probe_read_kernel_str(&fname, sizeof(fname), dentry->d_name.name);
    bpf_trace_printk("delete: %s\\n", fname);
    return 0;
}
"""

b = BPF(text=program)

print(f"Listening for deletion of '{TARGET_FILE}'... Ctrl+C to exit.")

while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue

    if TARGET_FILE.encode() in msg:
        print(f"File '{TARGET_FILE}' was deleted!")
