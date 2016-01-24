#!/usr/bin/bash

on_sigint() {
  echo "Script exit"
}

trap on_sigint 0

export LIBVIRT_DEFAULT_URI="qemu+tcp://admin:admin@127.0.0.1/system"

echo -e "$LIBVIRT_DOMAIN_XML" | virsh define -

virsh start "$LIBVIRT_DOMAIN"

virsh event --loop --all "$LIBVIRT_DOMAIN"
