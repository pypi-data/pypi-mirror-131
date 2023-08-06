# coding: utf8
import argparse
import logging
import logging.config
from ..api import Teachable


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Searches for users and returns a list''',
                                     epilog="""---""")
    parser.add_argument('-s', '--search', nargs=1,
                        help='What to search for (text contained in either email or user name)',
                        required=True)
    args = parser.parse_args()
    return args


def search_app(args):
    api = Teachable()
    logger = logging.getLogger(__name__)
    search = args.search[0]
    users = api.find_many_users(search)
    for user in users:
        print('{} <{}> - Enrolled in {}'.format(user.name, user.email,
                                                ['{} ({})'.format(t.name,t.id) for t in user.courses]))


def main():
    args = parse_arguments()
    search_app(args)


if __name__ == '__main__':
    main()
