strongarm-msdns
===============

strongarm-msdns is `STRONGARM <http://strongarm.io>`_'s Microsoft DNS
integration that updates DNS zones according to the list of blackholed domains
provided by the `STRONGARM API <https://strongarm.percipientnetworks.com/api/>`_.

features
--------

- fetch blackholed domains from STRONGARM API through 
  `stronglib <https://github.com/percipient/stronglib>`_.
- create DNS zones in Microsoft DNS to blackhole domains
- reload existing blackholed domains to different blackhole IP

installation
------------

strongarm-msdns is still in beta. The **latest development version** can be
installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade https://github.com/percipient/strongarm-msdns/tarball/master

A Windows installer or executable is coming soon.

usage
-----

.. code-block:: python

    from strongarm_msdns import MicrosoftDnsUpdater

    # Initialize updater with blackhole IP.
    dns_updater = MicrosoftDnsUpdater('127.0.0.1')

    # Run the updater with STRONGARM API key.
    dns_updater.run(your_key)

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
