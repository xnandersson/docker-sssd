====
SSSD
====

Repositories
------------

.. code:: bash

  $ git clone git@github.com:xnandersson/docker-dc.git
  $ git clone git@github.com:xnandersson/docker-sssd.git


Software Dependencies
---------------------

.. code:: bash

  $ sudo apt-get install docker.io python3-venv -yqq
  

Virtual Environment
-------------------

.. code:: bash

  $ python3 -m venv ~/venv3/docker-sssd
  $ source ~/venv3/docker-sssd/bin/activate
  (docker-sssd) $ pip install -r requirements.txt
  (docker-sssd) $ docker-compose up -d
  
  
Abstract
--------

Creates a Docker Image, preloaded with sssd, kerberos,  and an enroll-script
that joins the container on startup using the supplied variables.

The enrollment procedure ends with SSHD starting up, making the container available on port 22 (redirected to port 2223 in the example below). If you want to debug as root - start the container with a /bin/bash instead of /usr/local/bin/enroll.py, edit enroll.py and comment out the sshd() in the last row.

Start container and do the enroll procedure

.. code:: bash

  $ DC_IPADDR=$(docker inspect dc | grep IPAddr | egrep -o --regexp='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.[0-9]{1,3}' | head -1)
  $ sudo docker run \
      --rm \
      -ti \
      --dns=${DC_IPADDR} \
      --link dc:dc \
      -p 2223:22 \
      -e DEFAULT_REALM=OPENFORCE.ORG \
      -e ADMIN_SERVER=dc.openforce.org \
      -e KERBEROS_SERVERS=dc.openforce.org \
      xnandersson/sssd /usr/local/bin/enroll.py


