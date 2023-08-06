# coding: utf8
import argparse
import logging
import logging.config
from ..api import Teachable
from ..user import User
import sys
import os
from email.utils import formataddr
from ..utils.email_utils import Email
from ..utils.email_utils import EmailConnection
from ..utils.email_utils import render_template


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Change password for the user. \
                      If password is not set the system will generate a random one.''')
    parser.add_argument('-e', '--email', nargs=1,
                        help='The email of the user that you want to change.',
                        required=True)
    parser.add_argument('-p', '--password', nargs=1,
                        help='The new password for the user.')
    args = parser.parse_args()
    return args


def change_app(args):
    api = Teachable()
    logger = logging.getLogger(__name__)
    config = api.config
    #   override_mail = 'stefano.mosconi@britemind.io'
    defaults = config['DEFAULT']
    site_url = defaults['site_url']
    smtp_pwd = defaults['smtp_pwd']
    smtp_user = defaults['smtp_user']
    smtp_port = defaults['smtp_port']
    smtp_server = defaults['smtp_server']
    smtp_from = defaults['smtp_from']
    templates_dir = api.TEACHABLE_TEMPLATES_DIR
    email_addr = args.email[0]
    u = User(api, email_addr)
    if not u.exists:
        logger.error('No user found with email {}'.format(email_addr))
        sys.exit(9)
    try:
        if args.password is not None:
            password = u.change_password(args.password[0])
        else:
            password = u.change_password()
        logger.info('New password for user with email {}: {}'.format(u.email, password))
        logger.info('Connecting to email server ({})'.format(smtp_server))
        server_str = smtp_server + ':' + str(smtp_port)
        firstname = u.name.split()[0]
        from_addr = formataddr((smtp_from, smtp_user))
        to_addr = formataddr((u.name, u.email))
        cc_addr = None
        msg_dict = {'firstname': firstname,
                    'password': password,
                    'site_url': site_url,
                    'name_from': smtp_from}
        subject = 'Your password for {} has been changed'.format(site_url)
        message = render_template(os.path.join(templates_dir, 'change_password.txt'),
                                  msg_dict)
        if message:
            mail = Email(from_=from_addr, to=to_addr, cc=cc_addr,
                         subject=subject, message=message, message_encoding="utf-8")
            logger.info('Sending mail to {}'.format(to_addr))
            server = EmailConnection(server_str, smtp_user, smtp_pwd)
            server.send(mail, bcc=smtp_user)
            server.close()
    except Exception as e:
        logger.error(e)
        sys.exit(9)


def main():
    args = parse_arguments()
    change_app(args)


if __name__ == '__main__':
    main()
