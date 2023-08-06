# coding: utf8
import argparse
import logging
import logging.config
import enlighten
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
    parser = argparse.ArgumentParser(description='''Mass unenroll users from Excel or CSV file from a specified course.\
                                        Alternatively unenroll all users that have been enrolled for a certain amount \
                                        of days specified with -d option''',
                                     epilog="""---""")
    parser.add_argument('--dryrun', action='store_true',
                        default='False', help='''Don't send the messages for real, just do a dry run''')
    parser.add_argument('-i', '--input_file', nargs=1,
                        help='[Optional] Excel or CSV file. The only needed columns are \'fullname\' and \'email\' ')
    parser.add_argument('-c', '--courseId', type=str, nargs=1, help='[Optional] The id of the course they should be enrolled in')
    parser.add_argument('-d', '--days', help='''[Optional] Specifies the number of days after which a user will be unenrolled.\
                                                For instance -d 365 will unenroll every user that has been enrolled \
                                                for 366 days or more.
                                                IMPORTANT: This action cannot be recovered. Use at your own risk.''')
    args = parser.parse_args()

    if not args.courseId and not args.input_file and not args.days:
        print('ERROR - Please specify at least an argument\n')
        parser.print_help()
        sys.exit(2)

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
                    else:
                        logger.info('[DRYRUN] Not unenrolling for real {}'.format(u.name))


    elif args.days:
        all_users = api.get_all_users()
        manager = enlighten.get_manager()
        pbar = manager.counter(total=len(all_users), desc='Users', unit='users')
        for i in all_users:
            reportcard = i.reportcard
            for cid in reportcard:
                if cid != 'meta':
                    days_enrolled = reportcard[cid]['days_enrolled']
                    if days_enrolled > int(args.days):
                        course = Course(api, cid)
                        logger.info('Unenrolling {} from course {} (enrolled for {} days)'.format(i.name, course.name, days_enrolled))
                        if args.dryrun is not True:
                            i.unenroll(course)
                        else:
                            logger.info('[DRYRUN] Not unenrolling for real {}'.format(i.name))
                        message = ''
                        firstname = i.name.split()[0]
                        from_addr = formataddr((smtp_from, smtp_user))
                        to_addr = formataddr((i.name, i.email))
                        cc_addr = None
                        msg_dict = {'firstname': firstname, 'days':args.days, 'course': course.name, 'name_from': smtp_from}
                        subject = 'You have been unenrolled from the {course} course'.format(course=course.name)
                        message = render_template(os.path.join(templates_dir, 'unenroll.txt'),
                                                      msg_dict)
                        if message:
                            mail = Email(from_=from_addr, to=to_addr, cc=cc_addr,
                                         subject=subject, message=message, message_encoding="utf-8")
                            if args.dryrun is not True:
                                logger.info('Sending mail to {}'.format(to_addr))
                                server = EmailConnection(server_str, smtp_user, smtp_pwd)
                                server.send(mail, bcc=smtp_user)
                                server.close()
                            else:
                                logger.info('[DRYRUN] Not sending email to {}'.format(to_addr))
            pbar.update()




def main():
    args = parse_arguments()
    unenroll_app(args)


if __name__ == '__main__':
    main()
