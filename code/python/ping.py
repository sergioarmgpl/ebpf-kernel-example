from bcc import BPF

program = r"""
#include <uapi/linux/ptrace.h>
#include <linux/skbuff.h>

#define TASK_COMM_LEN 16

int kprobe____dev_queue_xmit(struct pt_regs *ctx, struct sk_buff *skb) {
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    if (comm[0] != 'p' || comm[1] != 'i' || comm[2] != 'n' || comm[3] != 'g' || comm[4] != '\0') {
        return 0;
    }

    u32 len = 0;
    bpf_probe_read_kernel(&len, sizeof(len), &skb->len);

    bpf_trace_printk("ping traffic pid=%d comm=%s len=%d\n",
                     bpf_get_current_pid_tgid() >> 32,
                     comm,
                     len);
    return 0;
}
"""

BPF(text=program).trace_print()
