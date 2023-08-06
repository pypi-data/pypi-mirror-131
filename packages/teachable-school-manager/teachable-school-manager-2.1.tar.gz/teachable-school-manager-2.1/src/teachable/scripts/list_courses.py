# coding: utf8
import argparse
import logging
import logging.config
from ..api import Teachable


def parse_arguments():
    parser = argparse.ArgumentParser(description='''List courses in school''',
                                     epilog="""---""")
    args = parser.parse_args()
    return args


def list_app(args):
    api = Teachable()
    logger = logging.getLogger(__name__)
    courses = api.courses
    for course in courses:
        print('{} ({}) [{} users enrolled] [{} users completed]'.format(course.name, course.id, len(course.users), len(course.completed)))


def main():
    args = parse_arguments()
    list_app(args)


if __name__ == '__main__':
    main()
