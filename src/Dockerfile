FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-21
RUN apt-get update -yqq
RUN apt-get install realmd dbus policykit-1 packagekit rsyslog inetutils.ping nmap vim smbclient cifs-utils ssh sssd sssd-tools adcli python3-jinja2 sudo -yqq
COPY templates /templates
ADD enroll.py /usr/local/bin/enroll.py
RUN chmod +x /usr/local/bin/enroll.py
RUN mkdir /run/sshd
EXPOSE 22
CMD /bin/bash
