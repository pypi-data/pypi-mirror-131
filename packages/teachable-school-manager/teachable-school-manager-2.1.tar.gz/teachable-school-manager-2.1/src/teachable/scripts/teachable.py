from ..scripts import unenroll, remind, user_report, statements, leaderboard, enroll, \
                      auto_unenroll, search_users, list_courses, change_password
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='\n*** Welcome to the command line interface to Teachable APIs. ***'\
                                     '\n\nThe available commands are the following:\n',  add_help=False)

    parser.add_argument('-h', '--help', action=_HelpAction, help='help for help if you need some help')  # add custom help

    subparser = parser.add_subparsers(dest='command')
    users = subparser.add_parser('users', description='''Searches for users and returns a list''')
    courses = subparser.add_parser('courses', description='''List courses in school''')

    enroll = subparser.add_parser('enroll', description='''Mass enroll users from Excel or CSV file into a specified course''')
    unenroll = subparser.add_parser('unenroll', description='Mass unenroll users from Excel or CSV file from a specified course. ')
    auto_unenroll = subparser.add_parser('auto_unenroll', description='Automatically unenroll all users that have been enrolled for a certain amount ' \
                                        'of days specified with -d option')
    remind = subparser.add_parser('remind', description='''Polls Teachable and sends '''\
                                'reminders to those that haven\'t started a course or haven\'t done a lesson'\
                                ''' in a week.''')
    statements = subparser.add_parser('statements', description='''Get the latest earning statement as Excel (default) or CSV. '''\
                                        '''Optionally send them over email to the school owner''')
    leaderboard = subparser.add_parser('leaderboard', description='''Get a Leaderboard CSV in just'''\
                        ''' one command. It will save as many leaderboards CSV as you have courses.''')
    user_report = subparser.add_parser('user_report', description='Get your Teachable students report. '\
                                       'By default, if no --emails or --search options are provided '\
                                       'it will generate a progress summary report of all the students that '\
                                       'are enrolled in all your courses. '\
                                       'This is very similar to using teachable leaderboard: while this allows to '\
                                       'specify a specific set of users, the other one allows to specify a course.'\
                                       'Pay attention if you have a lot of students '\
                                       'because this will be rate limited at some point.')

    leaderboard.add_argument('--search', '-s', nargs='?', default='',
                        help='''Searches specific text in the name of the course''')

    users.add_argument('-s', '--search', nargs=1,
                        help='What to search for (text contained in either email or user name)',
                        required=True)

    change_password = subparser.add_parser('password', description='''Change password for the user. \
                                        If password not set the system will generate a random one''')
    change_password.add_argument('-e', '--email', nargs=1,
                        help='The email of the user that you want to change.',
                        required=True)
    change_password.add_argument('-p', '--password', nargs=1,
                        help='The new password for the user.')

    statements.add_argument('--email', '-e',
                        action='store_true',
                        default='False', help='''Send the statements to the school owner''')
    statements.add_argument('--all', '-a',
                        action='store_true',
                        default='False', help='''Get all the statements, not just the last one''')
    statements.add_argument('--format', '-f', nargs='?', default='excel',
                        help='Output format (excel[default], csv)')
    statements.add_argument('--ofile', '-o', nargs='?', default='earnings_statement', help='Output file name')

    user_report_group = user_report.add_mutually_exclusive_group()
    user_report_group.add_argument('--emails', '-e', type=str, nargs='+', default='',
                       help='list of emails (separated by spaces)')
    user_report_group.add_argument('--search', '-s', nargs='?', default='',
                       help='''Searches specific text in name or email. For instance -s @gmail.com or \
                        -s *@gmail.com will look for all the users that have an email ending in \
                        @gmail.com. Or -s Jack will look for all the users that have Jack in \
                        their name (or surname)''')
    user_report.add_argument('--format', '-f', nargs='?', default='txt', help='Output format (excel, csv, txt [default])')
    user_report.add_argument('--courseid', '-c', nargs='?', default=0, help='''Limit
    search to this course id only (numeric value)''')
    user_report.add_argument('--output_file', '-o', nargs='?', default='teachable_stats', help='Output file')
    user_report.add_argument('--detailed', '-d', action='store_true', default='False',
                        help='Get detailed progress report')

    remind_group = remind.add_mutually_exclusive_group()
    remind_group.add_argument('--reportonly', '-r', action='store_true',
                        default='False', help='''Send the weekly report, 
                        not the notifications to all the users''')
    remind_group.add_argument('--notifyonly', '-n', action='store_true',
                        default='False', help='''Send the notifications to the users
                        not the weekly report''')
    remind.add_argument('--dryrun', '-d', action='store_true',
                        default='False', help='''Don't send the messages for 
                        real, just do a dry run''')

    enroll.add_argument('-i', '--input_file', nargs=1, type=str,
                        help='Excel or CSV file. The only needed columns are \'fullname\' and \'email\' ',
                        required=True)
    enroll.add_argument('-c', '--courseId', type=str, nargs=1, help='The id of the course they should be enrolled in',
                        required=True)
    enroll.add_argument('--dryrun', action='store_true',
                        default='False', help='''Don't send the messages for real, just do a dry run''')
    unenroll.add_argument('-i', '--input_file', nargs=1, type=str,
                        help='Excel or CSV file. The only needed columns are \'fullname\' and \'email\' ',
                          required=True)
    unenroll.add_argument('-c', '--courseId', type=str, nargs=1, help='The id of the course they should be enrolled in',
                          required=True)
    unenroll.add_argument('--dryrun', action='store_true',
                          default='False', help='''Don't send the messages for real, just do a dry run''')
    auto_unenroll.add_argument('-d', '--days', help='''Specifies the number of days after which a user will be unenrolled.\
                                                For instance -d 365 will unenroll every user that has been enrolled \
                                                for 366 days or more.
                                                IMPORTANT: This action cannot be recovered. Use at your own risk.''',
                               required=True)
    auto_unenroll.add_argument('--dryrun', action='store_true',
                        default='False', help='''Don't send the messages for real, just do a dry run''')


    # parser.add_argument('--hidefree', type=int, default=0, help='0: show/1: hide free courses ')



    #group.add_argument('--notifyonly', '-n', action='store_true',
    #                    default='False', help='''Send the notifications to the users
    #                    not the weekly report''')

    arguments = parser.parse_args()
    return arguments

def main():
    args = parse_arguments()
    if args.command == 'remind':
        remind.remind_app(args)
    elif args.command == 'unenroll':
        unenroll.unenroll_app(args)
    elif args.command == 'auto_unenroll':
        auto_unenroll.auto_unenroll_app(args)
    elif args.command == 'statements':
        statements.statements_app(args)
    elif args.command == 'enroll':
        enroll.enroll_app(args)
    elif args.command == 'leaderboard':
        leaderboard.leaderboard_app(args)
    elif args.command == 'user_report':
        user_report.report_app(args)
    elif args.command == 'users':
        search_users.search_app(args)
    elif args.command == 'courses':
        list_courses.list_app(args)
    elif args.command == 'password':
        change_password.change_app(args)
    return args

class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        #parser.print_help()
        print(parser.description)

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        import textwrap
        divider = '-'*80
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                com = subparser.format_usage().replace('usage: ', '')
                help = '''{}'''.format(subparser.description)
                help = textwrap.wrap(help, width=80, initial_indent='    ', subsequent_indent='    ',
                                     break_on_hyphens=True, drop_whitespace=True, expand_tabs=True,
                                     replace_whitespace=True,)
                print(com)
                for l in help:
                    print(l)
                print('\n{}\n'.format(divider))
        print('Run {} [subcommand] -h to get help on the subcommands'.format(sys.argv[0]))

                #print("Subparser '{}'".format(choice))


        parser.exit()

if __name__ == '__main__':
    main()
