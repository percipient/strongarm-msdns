strongarm-msdns
===============

strongarm-msdns is `STRONGARM <http://strongarm.io>`_'s Microsoft DNS
integration that updates DNS zones according to the list of blackholed domains
provided by the `STRONGARM API <https://strongarm.percipientnetworks.com/api/>`_.

.. image:: https://travis-ci.org/percipient/strongarm-msdns.svg?branch=master
    :target: https://travis-ci.org/percipient/strongarm-msdns

.. image:: https://coveralls.io/repos/percipient/strongarm-msdns/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/percipient/strongarm-msdns

features
--------

- fetch blackholed domains from STRONGARM API through
  `stronglib <https://github.com/percipient/stronglib>`_.
- create DNS zones in Microsoft DNS to blackhole domains
- reload existing blackholed domains to different blackhole IP

installation
------------

strongarm-msdns is still in beta. We plan to provide a pre-built Windows
installer to make the installation process easy. In the meantime:

1. Install `Python <https://www.python.org/downloads/>`_ and
   `pywin32 <http://sourceforge.net/projects/pywin32/files/>`_.

2. Install the **latest development version** of strongarm-msdns directly from
   GitHub using pip:

.. code-block:: bash

    $ pip install --upgrade https://github.com/percipient/strongarm-msdns/tarball/master

usage
-----

We plan to provide a Windows service that runs the updater automatically. In
the meantime, you can run the updater manually in Python on a Microsoft DNS
server with WMI enabled:

.. code-block:: python

    from strongarm_msdns.msdns import MicrosoftDnsUpdater

    # Initialize updater with blackhole IP.
    dns_updater = MicrosoftDnsUpdater('127.0.0.1')

    # Run the updater with STRONGARM API key.
    dns_updater.run(your_key)

DNS zones will be created for all domains fetched from the STRONGARM API. The
call returns a list of domain names that failed to be blackholed.

contribute
----------

#. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
#. If you feel uncomfortable or uncertain about an issue or your changes,
   feel free to email @dicato and he will happily help you.
#. Fork `the repository`_ on GitHub to start making your changes to the
   **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature
   works as expected.
#. Send a pull request and bug the maintainer until it gets merged and
   published. :) Make sure to add yourself to AUTHORS_.

.. _the repository: http://github.com/percipient/strongarm-msdns
.. _AUTHORS: https://github.com/percipient/strongarm-msdns/blob/master/AUTHORS.rst
