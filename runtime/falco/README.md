# Falco Runtime Example

This folder contains a simple example of running Falco in Docker to monitor system activity from the host.

## Commands to run

Start Falco in Docker with privileged access and mount the required host paths:

```bash
docker run --rm -it \
  --name falco \
  --privileged \
  -v /sys/kernel/tracing:/sys/kernel/tracing:ro \
  -v /var/run/docker.sock:/host/var/run/docker.sock \
  -v /proc:/host/proc:ro \
  -v /etc:/host/etc:ro \
  falcosecurity/falco:0.44.1
```

This command starts Falco interactively and removes the container when it exits.

## What this does

The Falco container is started with privileged access and mounts key host paths so it can monitor system calls, container activity, and host metadata.

The mounted paths are:

- `/sys/kernel/tracing:/sys/kernel/tracing:ro`
- `/var/run/docker.sock:/host/var/run/docker.sock`
- `/proc:/host/proc:ro`
- `/etc:/host/etc:ro`

The container image used in this example is `falcosecurity/falco:0.44.1`.

## Simulate suspicious activity

After Falco is running, you can produce a suspicious event such as reading the host shadow file:

```bash
sudo cat /etc/shadow
```

Falco is often configured to alert on such sensitive host file access.

## Notes

- Run Docker with sufficient privileges so Falco can access host tracing and process information.
- If you want to keep Falco running in the background, remove `-it` and add `-d`.
- The Docker socket mount allows Falco to correlate container activity with running Docker containers.
