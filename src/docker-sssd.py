#!/usr/bin/env python
import docker
import os
import uuid

BUILD_DIR = '/tmp/{uuid}/'.format(uuid=uuid.uuid4().hex)

def mkdir_build_dir():
    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError as e:
        pass

def create_enroll():
    with open(os.path.join(BUILD_DIR, 'enroll'), 'w') as f:
            f.write("""#!/bin/bash
if [ ! -f /etc/krb5.conf ]; then
  apt-get update -y
  cat << EOF > /tmp/krb5-config.debconf
krb5-config krb5-config/default_realm   string  ${DEFAULT_REALM}
krb5-config krb5-config/admin_server    string  ${ADMIN_SERVER}
krb5-config krb5-config/kerberos_servers    string  ${KERBEROS_SERVERS}
EOF
  export DEBIAN_FRONTEND="noninteractive"
  debconf-set-selections /tmp/krb5-config.debconf
  apt-get install krb5-user -yqq
  cat << EOF > /etc/krb5.conf
[libdefaults]
    default_realm = ${DEFAULT_REALM}
    dns_lookup_realm = false
    dns_lookup_kdc = true
EOF
fi
""")

def create_dockerfile():
    with open(os.path.join(BUILD_DIR, 'Dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-21
RUN apt-get update -yqq
RUN apt-get install realmd dbus policykit-1 packagekit rsyslog inetutils.ping nmap vim smbclient cifs-utils ssh sssd sssd-tools adcli -yqq
ADD enroll /usr/local/bin/enroll
RUN chmod +x /usr/local/bin/enroll
RUN mkdir /run/sshd
EXPOSE 22
CMD /bin/bash""")

if __name__ == '__main__':
    mkdir_build_dir()
    create_enroll()
    create_dockerfile()
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    client.images.build(path=BUILD_DIR, tag='xnandersson/sssd', rm=True, pull=True)
