====
SSSD
====

Abstract
--------

Docker Image with sssd, kerberos and enroll.py that joins the container on startup using the supplied variables.

Enrollment procedure ends with SSHD starting up, making the container available on port 22 (redirected to port 2223 in the example below). If you want to debug as root - start the container with a /bin/bash instead of /usr/local/bin/enroll.py, edit enroll.py and comment out the sshd() in the last row.


Repositories
------------

.. code:: bash

  $ git clone git@github.com:xnandersson/docker-dc.git
  $ docker build -t xnandersson/samba-ad-dc .
  $ git clone git@github.com:xnandersson/docker-slapd.git
  $ docker build -t xnandersson/slapd .
  $ git clone git@github.com:xnandersson/docker-sssd.git
  $ docker build -t xnandersson/sssd .


Slapd
-----

.. code:: bash

  $ sudo docker run \
  --name slapd \
  --rm \
  -d \
  -e DOMAIN=openforce.org \
  -e PASSWORD=Secret007! \
  -e ORGANIZATION="Openforce AB" \
  -p 3389:389 \
  xnandersson/slapd

Active Directory
----------------

.. code:: bash

  $ sudo docker run \
      --privileged \
      --name dc \
      --rm \
      -d \
      -e SAMBA_DOMAIN=openforce \
      -e SAMBA_HOST_NAME=dc \
      -e SAMBA_ADMINPASS=Abc123! \
      -e SAMBA_KRBTGTPASS=Abc123! \
      -e SAMBA_REALM=OPENFORCE.ORG \
      -p 2222:22 -p 5353:53 -p 88:88 \
      -p 135:135 -p 139:139 -p 389:389 \
      -p 445:445 -p 464:464 -p 636:636 \
      -p 1024:1024 -p 3268:3268 -p 3269:3269 \
      xnandersson/samba-ad-dc /usr/local/bin/dcpromo.py
  
  $ docker exec dc samba-tool user create nandersson Secret012
  
SSSD
----
  
.. code:: bash

  $ DC_IPADDR=$(docker inspect dc | grep IPAddr | egrep -o --regexp='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.[0-9]{1,3}' | head -1)
  
  $ sudo docker run \
      --name sssd \
      --rm \
      -ti \
      --dns=${DC_IPADDR} \
      --link dc:dc \
      --link slapd:slapd \
      -p 2223:22 \
      -e DEFAULT_REALM=OPENFORCE.ORG \
      -e ADMIN_SERVER=dc.openforce.org \
      -e KERBEROS_SERVERS=dc.openforce.org \
      xnandersson/sssd /usr/local/bin/enroll.py
  $ ssh -p 2223 nandersson@127.0.0.1 # user/pass nandersson/Secret012


