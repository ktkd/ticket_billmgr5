#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file to get config from environment variables
"""
import os
from collections import namedtuple

TicketCfg = namedtuple('ticketcfg',
                       ' tickets_url'
                       ' tickets_user'
                       ' tickets_pass'
                       ' tickets_timeout'
                       ' tickets_print'
                       ' tickets_webhook'
                       ' tickets_webhook_url'
                       ' tickets_webhook_token')
CONF = TicketCfg(tickets_url=os.environ['tickets_url'],
                 tickets_user=os.environ['tickets_user'],
                 tickets_pass=os.environ['tickets_pass'],
                 tickets_timeout=os.environ['tickets_timeout'],
                 tickets_print=os.environ['tickets_print'],
                 tickets_webhook=os.environ['tickets_webhook'],
                 tickets_webhook_url=os.environ['tickets_webhook_url'],
                 tickets_webhook_token=os.environ['tickets_webhook_token'])
