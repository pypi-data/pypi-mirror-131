# coding: utf8
import argparse
import logging
import logging.config
import sys
import os


import pyexcel as px

from email.utils import formataddr

from ..utils.email_utils import Email
from ..utils.email_utils import EmailConnection
from ..utils.email_utils import render_template

from ..api import Teachable
from ..course import Course
from ..user import User


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Mass unenroll users from Excel or CSV file from a specified course.''',
                                     epilog="""---""")
    parser.add_argument('--dryrun', action='store_true',
                        default='False', help='''Don't send the messages for real, just do a dry run''')
    parser.add_argument('-i', '--input_file', nargs=1,
                        help='Excel or CSV file. The only needed columns are \'fullname\' and \'email\' ',
                        required=True)
    parser.add_argument('-c', '--courseId', type=str, nargs=1,
                        help='The id of the course they should be enrolled in', required=True)
    args = parser.parse_args()

    return args


def unenroll_app(args):
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
    logger.info('Connecting to email server ({})'.format(smtp_server))
    server_str = smtp_server + ':' + str(smtp_port)
    if args.courseId and args.input_file:
        course_id = args.courseId[0]
        input_file = args.input_file[0]
        records = px.get_records(file_name=input_file)
        for user in records:
            # search if the user with the given email exists
            if user['email'] != '':
                u = User(api, user['email'])
                course = Course(api, course_id)
                if u.exists:
                    if args.dryrun is not True:
                        resp = u.unenroll(course)
                        if 'message' in resp.keys():
                            logger.info(resp['message'])
                        else:
                            logger.info(u.name + ' unenrolled')
                            logger.info('Unenrolling {} from course {}'.format(u.name, course.name))
                            message = ''
                            firstname = u.name.split()[0]
                            from_addr = formataddr((smtp_from, smtp_user))
                            to_addr = formataddr((u.name, u.email))
                            cc_addr = None
                            msg_dict = {'firstname': firstname, 'course': course.name,
                                        'name_from': smtp_from}
                            subject = 'You have been unenrolled from the {course} course'.format(course=course.name)
                            message = render_template(os.path.join(templates_dir, 'unenroll.txt'),
                                                      msg_dict)
                            if message:
                                mail = Email(from_=from_addr, to=to_addr, cc=cc_addr,
                                             subject=subject, message=message, message_encoding="utf-8")
                                logger.info('Sending mail to {}'.format(to_addr))
                                server = EmailConnection(server_str, smtp_user, smtp_pwd)
                                server.send(mail, bcc=smtp_user)
                                server.close()
                    else:
                        logger.info('[DRYRUN] Not unenrolling for real {}'.format(u.name))



def main():
    args = parse_arguments()
    unenroll_app(args)


if __name__ == '__main__':
    main()
