# Tetragon Runtime Example

This folder contains documentation for running Tetragon in Docker to monitor host activity using a Tetragon policy file.

## Commands to run

Stop any existing Tetragon container first:

```bash
docker stop tetragon
```

Then start Tetragon with privileged access and the policy file mounted into the container:

```bash
docker run -d --name tetragon --rm --pull always \
  --pid=host --cgroupns=host --privileged \
  -v ${PWD}/file_monitoring.yaml:/etc/tetragon/tetragon.tp.d/file_monitoring.yaml \
  -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
  quay.io/cilium/tetragon:v1.7.0
```

This command launches the Tetragon container so it can monitor the host using the provided policy.

## How to inspect events

Once Tetragon is running, use the `tetra getevents` command inside the container to view detected events:

```bash
docker exec -ti tetragon tetra getevents -o compact
```

This prints events in compact form as Tetragon observes activity.

## Simulate suspicious activity

To generate sample activity that Tetragon can monitor, run an interactive container and perform a sensitive host operation:

```bash
docker run -it --rm alpine /bin/sh
cat /etc/shadow
```

The mounted policy can be configured to alert on file access or other suspicious behavior.

## Notes

- `file_monitoring.yaml` must exist in the same directory where the Docker command is run.
- The `vmlinux` BTF file is mounted from the host to provide kernel metadata to Tetragon.
- Run Docker with sufficient privileges so Tetragon can access host namespaces and tracing information.
