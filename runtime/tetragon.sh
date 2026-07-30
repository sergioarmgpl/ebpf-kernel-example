https://tetragon.io/docs/getting-started/install-docker/

#wget https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/file_monitoring.yaml
docker stop tetragon
docker run -d --name tetragon --rm --pull always \
  --pid=host --cgroupns=host --privileged \
  -v ${PWD}/file_monitoring.yaml:/etc/tetragon/tetragon.tp.d/file_monitoring.yaml \
  -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
  quay.io/cilium/tetragon:v1.7.0

docker exec -ti tetragon tetra getevents -o compact


docker run -it --rm alpine /bin/sh

cat /etc/shadow

