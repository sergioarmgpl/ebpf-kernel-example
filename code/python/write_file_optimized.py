from bcc import BPF

# File we want to monitor
TARGET_FILE = "test.txt"
TARGET_LEN = len(TARGET_FILE)

program = f"""
#include <linux/fs.h>

#define TARGET_LEN {TARGET_LEN}

static const char target[TARGET_LEN] = "{TARGET_FILE}";

int kprobe__vfs_write(struct pt_regs *ctx, struct file *file, const char __user *buf, size_t count) {{
    char fname[TARGET_LEN + 1] = {{}};

    bpf_probe_read_kernel_str(&fname, sizeof(fname), file->f_path.dentry->d_name.name);

    // Byte-by-byte comparison unrolled at compile time
    #pragma unroll
    for (int i = 0; i < TARGET_LEN; i++) {{
        if (fname[i] != target[i]) {{
            return 0;
        }}
    }}

    // Verify the name ends exactly there (avoids matching "test.txt2")
    if (fname[TARGET_LEN] != '\\0') {{
        return 0;
    }}

    bpf_trace_printk("Detected write to target file: %s\n", fname);
    return 0;
}}
"""

b = BPF(text=program)

print(f"Listening for writes to '{TARGET_FILE}' (kernel filtered)... Ctrl+C to exit.")
b.trace_print()
