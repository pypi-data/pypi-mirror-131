import schedule
import time
import subprocess
from ..api import Teachable
from ..utils.common import get_config
import os
from configparser import ConfigParser
import logging

api = Teachable()
# This is the template for all the scheduler fucntions we are going to run
# They are defined dynamically based on the scheduler.ini config file
func_template = '''def {}(): subprocess.run(["{}", "{}"]); return'''
main_func_template = '''schedule.every({}).{}{}.do({})'''
logger = logging.getLogger(__name__)
conf_file = os.path.join(api.DEFAULT_DIRS['TEACHABLE_ETC_DIR'], 'scheduler.ini')
# If we don't free up the api object nothing else will run because all the
# status databases are not going to open...
del api

conf = get_config(conf_file)


if conf:
    for f in conf.sections():
        logger.debug('defining function {}'.format(f))
        logger.debug(func_template.format(f,conf[f]['script'],conf[f]['opts']))
        exec(func_template.format(f,conf[f]['script'],conf[f]['opts']))


def main():
    # No config file no party
    logger = logging.getLogger(__name__)
    if conf:
        for f in conf.sections():
            logger.debug('Forking {}'.format(f))
            logger.debug(main_func_template.format(conf[f]['every'], conf[f]['when'],
                                                   '.at("' + conf[f]['at_when'] + '")' if conf[f]['at_when'] else '', f))
            exec(main_func_template.format(conf[f]['every'], conf[f]['when'],
                                           '.at("' + conf[f]['at_when'] + '")' if conf[f]['at_when'] else '', f))

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()
