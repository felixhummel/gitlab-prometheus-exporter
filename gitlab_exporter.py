#!/usr/bin/env python
# encoding: utf-8

import logging
import os
import time

import gitlab
from prometheus_client import start_http_server, Gauge

try:
    loglevel = getattr(logging, os.environ.get('LOGLEVEL', 'WARN').upper())
except AttributeError:
    pass

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(level=loglevel)

# time to sleep between calls to gitlab
INTERVAL = int(os.environ.get('INTERVAL', 300))

# port to listen on
PORT = int(os.environ.get('PORT', 3001))

# This expects a valid config with default server. See
# http://python-gitlab.readthedocs.io/en/stable/cli.html#configuration
gl = gitlab.Gitlab.from_config()

sidekiq_jobs_enqueued = Gauge('sidekiq_jobs_enqueued', 'Total number of enqueued Sidekiq jobs')
sidekiq_jobs_failed = Gauge('sidekiq_jobs_failed', 'Total number of failed Sidekiq jobs')
sidekiq_jobs_processed = Gauge('sidekiq_jobs_processed', 'Total number of processed Sidekiq jobs')
gitlab_project_count = Gauge('gitlab_project_count', 'Number of projects')


def get_stats():
    log.info('fetching project count')
    gitlab_project_count.set(int(gl._raw_get('/projects/all').headers['X-Total']))
    x = gl.sidekiq.job_stats()
    # {'jobs': {'enqueued': 0, 'failed': 140300, 'processed': 211394}}
    sidekiq_jobs_enqueued.set(x['jobs']['enqueued'])
    sidekiq_jobs_failed.set(x['jobs']['failed'])
    sidekiq_jobs_processed.set(x['jobs']['processed'])


if __name__ == '__main__':
    start_http_server(PORT)
    log.info('listening on port {0}'.format(PORT))
    while True:
        try:
            get_stats()
            log.info('sleeping for {0} seconds'.format(INTERVAL))
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            break
