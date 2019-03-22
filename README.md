=========================================
SSSD
=========================================

Abstract
--------

Creates a Docker Image, preloaded with sssd, kerberos,  and an enroll-script
that joins the container on startup using the supplied variables.

Start container and do the enroll procedure

.. code:: bash

  $ docker run \
      --rm \
      -ti \
      -e SAMBA_DOMAIN=openforce \
      -e SAMBA_HOST_NAME=dc \
      -e SAMBA_ADMINPASS=Abc123! \
      -e SAMBA_KRBTGTPASS=Abc123! \
      -e SAMBA_REALM=OPENFORCE.ORG \
      xnandersson/sssd /usr/local/bin/enroll


Prerequisites
-------------

.. code:: bash

  $ sudo apt-get install docker.io python3-venv
  $ sudo usermod -a -G docker nandersson
  $ docker pull ubuntu:latest
