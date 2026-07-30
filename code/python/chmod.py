from bcc import BPF

# Archivo que queremos monitorear
TARGET_FILE = "test.txt"

program = r"""
#include <linux/fs.h>
#include <linux/path.h>

int kprobe__security_path_chmod(struct pt_regs *ctx, const struct path *path, umode_t mode) {
    char fname[64];
    bpf_probe_read_kernel_str(&fname, sizeof(fname), path->dentry->d_name.name);
    bpf_trace_printk("chmod: %s\\n", fname);
    return 0;
}
"""

b = BPF(text=program)

print(f"Escuchando cambios de permisos en '{TARGET_FILE}'... Ctrl+C para salir.")

while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue

    if TARGET_FILE.encode() in msg:
        print(f"Permissions changed for '{TARGET_FILE}'!")
