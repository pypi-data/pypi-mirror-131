#!/usr/bin/env python
# coding: utf-8

# This little project is hosted at: <https://gist.github.com/1455741>
# Copyright 2011-2020 Álvaro Justen [alvarojusten at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

import os
import sys
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type
from smtplib import SMTP
import logging
from configparser import ConfigParser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_config(configfile):
    """Gets config options"""
    if os.path.exists(configfile):
        logger.debug('Found config file at {}'.format(configfile))
        config = ConfigParser()
        config.read(configfile)
    else:
        logger.error('Config file not found: {}. Please create and restart.'.format(configfile))
        config = None
    return config