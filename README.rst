**************************
Prometheus Gitlab Exporter
**************************
This uses `Gitlab <https://gitlab.com>`__'s API to fetch some data and exposes
it to `Prometheus <https://prometheus.io/>`__.


Getting Started
===============
::

    ./gitlab_exporter.py

::

    curl localhost:3001


Config
======
The following environment variables may be set::

    LOGLEVEL=INFO PORT=3002 INTERVAL=180 ./gitlab_exporter.py

====================  ===========
Environment Variable  Description
====================  ===========
LOGLEVEL              Standard Python `log level`_
PORT                  Port to listen on
INTERVAL              Interval in seconds to wait between data fetches
====================  ===========

.. _log level: https://docs.python.org/3.5/library/logging.html#levels


Notes
=====
Please note that this fetches **all** projects. This may take a while and
produces load on your Gitlab instance. For 300 projects it took 10 seconds on
my server.

There are efforts for native Prometheus integration in Gitlab, e.g.
https://gitlab.com/gitlab-org/gitlab-workhorse/issues/61


Gitlab API
----------
- REST API Reference https://github.com/gitlabhq/gitlabhq/tree/master/doc/api
- Python API http://python-gitlab.readthedocs.io/en/stable/api-usage.html


Prometheus Exporter
-------------------
https://github.com/prometheus/client_python

