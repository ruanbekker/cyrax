#!/bin/sh
# https://raw.githubusercontent.com/docker-library/docker/master/modprobe.sh
set -eu

for module; do
	if [ "${module#-}" = "$module" ]; then
		ip link show "$module" || true
		lsmod | grep "$module" || true
	fi
done

export PATH='/usr/sbin:/usr/bin:/sbin:/bin'
exec modprobe "$@"

