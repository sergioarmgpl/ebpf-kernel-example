from bcc import BPF

# Archivo que queremos monitorear
TARGET_FILE = "test.txt"
TARGET_LEN = len(TARGET_FILE)

program = f"""
#include <linux/fs.h>

#define TARGET_LEN {TARGET_LEN}

static const char target[TARGET_LEN] = "{TARGET_FILE}";

int kprobe__vfs_write(struct pt_regs *ctx, struct file *file, const char __user *buf, size_t count) {{
    char fname[TARGET_LEN + 1] = {{}};

    bpf_probe_read_kernel_str(&fname, sizeof(fname), file->f_path.dentry->d_name.name);

    // Comparación byte a byte, desenrollada en tiempo de compilación
    #pragma unroll
    for (int i = 0; i < TARGET_LEN; i++) {{
        if (fname[i] != target[i]) {{
            return 0;
        }}
    }}

    // Verificamos que el nombre termine justo ahí (evita que "test.txt2" haga match)
    if (fname[TARGET_LEN] != '\\0') {{
        return 0;
    }}

    bpf_trace_printk("Escritura detectada en archivo objetivo: %s\\n", fname);
    return 0;
}}
"""

b = BPF(text=program)

print(f"Escuchando escrituras al archivo '{TARGET_FILE}' (filtrado en kernel)... Ctrl+C para salir.")
b.trace_print()
