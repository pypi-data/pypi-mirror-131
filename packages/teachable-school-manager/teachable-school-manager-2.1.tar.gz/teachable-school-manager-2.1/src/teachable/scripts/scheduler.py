import schedule
from ..api import Teachable
from ..utils.common import get_config
import logging
import time
import os
import sys
import subprocess

# This is the template for all the scheduler functions we are going to run
# They are defined dynamically based on the scheduler.ini config file
func_template = '''global {}\ndef {}(): subprocess.run(["{}", "{}"]); return'''
main_func_template = '''schedule.every({}).{}{}.do({})'''


def get_conf_path():
    api = Teachable()
    conf_file = os.path.join(api.DEFAULT_DIRS['TEACHABLE_ETC_DIR'], 'scheduler.ini')
    # If we don't free up the api object nothing else will run because all the
    # status databases are not going to open...
    del api
    return conf_file


def def_function(conf: str, logger: logging.Logger):
    for f in conf.sections():
        logger.debug('defining function {}'.format(f))
        logger.debug(func_template.format(f, f, conf[f]['script'], conf[f]['opts']))
        exec(func_template.format(f, f, conf[f]['script'], conf[f]['opts']))


def is_modified(file: str, last: str):
    if int(get_mod_time(file)) > int(last):
        return True
    else:
        return False


def get_mod_time(file: str):
    stat = os.stat(file)
    return stat.st_mtime


def spawn_from_conf(conf: str, logger: logging.Logger):
    for f in conf.sections():
        logger.debug('Forking {}'.format(f))
        logger.debug(main_func_template.format(conf[f]['every'], conf[f]['when'],
                                               '.at("' + conf[f]['at_when'] + '")' if conf[f]['at_when'] else '', f))
        exec(main_func_template.format(conf[f]['every'], conf[f]['when'],
                                       '.at("' + conf[f]['at_when'] + '")' if conf[f]['at_when'] else '', f))


def main():
    # No config file no party
    conf_file = get_conf_path()
    logger = logging.getLogger(__name__)
    if os.path.exists(conf_file):
        mod_time = get_mod_time(conf_file)
        conf = get_config(conf_file)
        def_function(conf, logger)
        spawn_from_conf(conf, logger)
        while True:
            if is_modified(conf_file, mod_time):
                logger.info('Config file {} modified - Reloading'.format(conf_file))
                # We keep checking every second whether the conf_file
                # has been modified and if so redefine the functions
                # Getting the new configuration
                conf = get_config(conf_file)
                # Clearing previously defined jobs
                schedule.clear()
                # Re-defining jobs
                def_function(conf, logger)
                spawn_from_conf(conf, logger)
                # Updating the latest modification time
                mod_time = get_mod_time(conf_file)
            schedule.run_pending()
            time.sleep(1)
    else:
        logger.error('Scheduler config file {} does not exist. Exiting.'.format(conf_file))
        sys.exit(9)


if __name__ == "__main__":
    main()
