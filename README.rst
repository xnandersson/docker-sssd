====
SSSD
====

Abstract
--------

Creates a Docker Image, preloaded with sssd, kerberos,  and an enroll-script
that joins the container on startup using the supplied variables.

Start container and do the enroll procedure

.. code:: bash

  $ docker run \
      --rm \
      -ti \
      -e DEFAULT_REALM=OPENFORCE.ORG \
      -e ADMIN_SERVER=dc.openforce.org \
      -e KERBEROS_SERVERS=dc.openforce.org \
      xnandersson/sssd /usr/local/bin/enroll


Prerequisites
-------------

.. code:: bash

  $ sudo apt-get install docker.io python3-venv
  $ sudo usermod -a -G docker nandersson
  $ docker pull ubuntu:latest
