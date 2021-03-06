#!/usr/bin/env python3
from jinja2 import Template
import os
import subprocess
from subprocess import PIPE, STDOUT 

DEFAULT_REALM = os.getenv('DEFAULT_REALM', 'ACME.ORG')
ADMIN_SERVER = os.getenv('ADMIN_SERVER', 'dc.acme.org')
KERBEROS_SERVERS = os.getenv('KERBEROS_SERVERS', ADMIN_SERVER)
DC_ENV_SAMBA_ADMINPASS = os.getenv('DC_ENV_SAMBA_ADMINPASS', 'Abc123!')

def install_kerberos(default_realm=None, admin_server=None, kerberos_servers=None):
    t = Template(open('/templates/krb5-config.debconf.jinja2').read())
    with open('/tmp/krb5-config.debconf', 'w') as f:
        f.write(t.render(
                    default_realm = default_realm,
                    admin_server = admin_server,
                    kerberos_servers = kerberos_servers))
    proc = subprocess.Popen(['debconf-set-selections', '/tmp/krb5-config.debconf'], stderr=open(os.devnull, 'w'))
    proc.wait()
    proc = subprocess.Popen(['apt-get', 'install', 'krb5-user', '-y'], stderr=open(os.devnull, 'w'))
    proc.wait()
    t = Template(open('/templates/krb5.conf.jinja2').read())
    with open('/etc/krb5.conf', 'w') as f:
        f.write(t.render(
                    default_realm = default_realm))

def fetch_kerberos_ticket(realm=None, password=None):
    proc = subprocess.Popen(['kinit', 'Administrator@{}'.format(realm)], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = proc.communicate(input=str.encode(password))
    proc.wait()

def configure_realmd(default_realm=None):
    t = Template(open('/templates/realmd.conf.jinja2').read())
    with open('/etc/realmd.conf', 'w') as f:
        f.write(t.render(
                    default_realm = default_realm))

def join(domain=None):
    proc = subprocess.Popen(['realm', '-v', 'join', domain])
    rc = proc.wait()
    return True if rc == 0 else False

def configure_sssd_conf(domain=None):
    t = Template(open('/templates/sssd.conf.jinja2').read())
    with open('/etc/sssd/sssd.conf', 'w') as f:
        f.write(t.render(
                default_realm=domain))
    proc = subprocess.Popen(['chmod', '0600', '/etc/sssd/sssd.conf'])
    proc.wait()

def service_start(service):
    proc = subprocess.Popen(['service', service, 'start'])
    rc = proc.wait()
    return True if rc == 0 else False

def service_restart(service):
    proc = subprocess.Popen(['service', service, 'restart'])
    rc = proc.wait()
    return True if rc == 0 else False

def configure_mkhomedir():
    with open('/usr/share/pam-configs/mkhomedir', 'w') as f:
        f.write("""Name: mkhomedir
Default: yes
Priority: 0
Session-Type: Additional
Session:
 required pam_mkhomedir.so skel=/etc/skel umask=0027
""")
    proc = subprocess.Popen(['debconf-set-selections'], stdin=PIPE)
    output = proc.communicate(input=str.encode('libpam-runtime libpam-runtime/profiles multiselect mkhomedir'))
    proc.wait()
    proc = subprocess.Popen(['rm', '/etc/pam.d/common-session', '/etc/pam.d/common-session-noninteractive'])
    proc.wait()
    my_env = os.environ.copy()
    my_env["DEBIAN_FRONTEND"] = "noninteractive"
    proc = subprocess.Popen(['pam-auth-update', '--force'], env=my_env)
    proc.wait()

def sshd():
    proc = subprocess.Popen(['/usr/sbin/sshd', '-D'])
    proc.wait()

if __name__ == '__main__':
    install_kerberos(
        default_realm=DEFAULT_REALM, admin_server=ADMIN_SERVER, kerberos_servers=KERBEROS_SERVERS) 
    service_start('rsyslog')
    service_start('dbus')
    fetch_kerberos_ticket(realm=DEFAULT_REALM, password=DC_ENV_SAMBA_ADMINPASS)
    configure_realmd(default_realm=DEFAULT_REALM)
    join(domain=DEFAULT_REALM)
    configure_mkhomedir()
    configure_sssd_conf(domain=DEFAULT_REALM)
    service_restart('sssd')
    sshd()
