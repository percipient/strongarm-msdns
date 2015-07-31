strongarm-msdns
============

[STRONGARM](http://strongarm.io)'s Microsoft DNS integration updates DNS
zones according to the list of blackholed domains provided by the
[STRONG API](https://strongarm.percipientnetworks.com/api/).

features
--------

- fetch blackholed domains from STRONGARM API through stronglib
- create DNS zones in Microsoft DNS to blackhole domains
- reload existing blackholed domains to different blackhole IP

installation
------------

To install strongarm-msdns, simply:

.. code-block:: bash

    $ pip install strongarm-msdns

A Windows installer or executable is coming soon.

usage
-----

.. code-block:: python

    # token authentication
    >>> from strongarm-msdns.core import strongarm-msdns
    >>> strong = strongarm-msdns(your_api_token)

    # list all blackholed domains
    >>> strong.get_domains()
    [u'example.com', u'example.org']


documentation
-------------

Documentation is available at ...

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

.. _`the repository`: http://github.com/percipient/strongarm-msdns
.. _AUTHORS: https://github.com/percipient/strongarm-cli/blob/master/AUTHORS.rst
