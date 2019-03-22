#!/usr/bin/env python
import docker
import os
import shutil
import uuid

BUILD_DIR = '/tmp/{uuid}/'.format(uuid=uuid.uuid4().hex)

def mkdir_build_dir():
    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError as e:
        pass

def copy_files_to_build_dir():
    shutil.copyfile('enroll.py', os.path.join(BUILD_DIR, 'enroll.py'))
    shutil.copyfile('sssd.conf.jinja2', os.path.join(BUILD_DIR, 'sssd.conf.jinja2'))
    shutil.copyfile('realmd.conf.jinja2', os.path.join(BUILD_DIR, 'realmd.conf.jinja2'))
    shutil.copyfile('krb5.conf.jinja2', os.path.join(BUILD_DIR, 'krb5.conf.jinja2'))
    shutil.copyfile('krb5-config.debconf.jinja2', os.path.join(BUILD_DIR, 'krb5-config.debconf.jinja2'))

def create_dockerfile():
    with open(os.path.join(BUILD_DIR, 'Dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-21
RUN apt-get update -yqq
RUN apt-get install realmd dbus policykit-1 packagekit rsyslog inetutils.ping nmap vim smbclient cifs-utils ssh sssd sssd-tools adcli python3-jinja2 -yqq
ADD enroll.py /usr/local/bin/enroll.py
ADD sssd.conf.jinja2 /tmp/sssd.conf.jinja2
ADD realmd.conf.jinja2 /tmp/realmd.conf.jinja2
ADD krb5-config.debconf.jinja2 /tmp/krb5-config.debconf.jinja2
ADD krb5.conf.jinja2 /tmp/krb5.conf.jinja2
RUN chmod +x /usr/local/bin/enroll.py
RUN mkdir /run/sshd
EXPOSE 22
CMD /bin/bash""")

if __name__ == '__main__':
    mkdir_build_dir()
    copy_files_to_build_dir()
    create_dockerfile()
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    client.images.build(path=BUILD_DIR, tag='xnandersson/sssd', rm=True, pull=True)
