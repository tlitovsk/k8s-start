FROM fabiand/libvirtd:latest

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y automake \
autoconf \
make \
libguestfs-tools \
qemu-system-x86 \
python-requests \
python-sh \
git \
glusterfs \
grubby \
kpartx \
squashfs-tools \
sudo \
libvirt \
libvirt-python \
libvirt-python3 \
lorax \
python-nose \
python-pyflakes \
python-pep8 \
virt-install \
rpm-build \
createrepo

ADD build-ngn.sh /

CMD ["/build-ngn.sh"]

# vim: et sts=4 sw=4:
