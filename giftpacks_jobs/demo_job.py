#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-11-22 11:44
# @Author  : ziyezhang

from public.GiftPacks import job_scheduler
from public.logger import Logger

logger = Logger(__name__)


def job_name():
    logger.info("job running")


job_scheduler.add_job(job_name, 'interval', minutes=5, id="job_name")

