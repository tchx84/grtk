#!/usr/bin/env python

# Copyright (c) 2013 Martin Abente Lahaye. - martin.abente.lahaye@gmail.com
# Copyright (c) 2013 Arturo Volpe Torres. - arturovolpe@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from argparse import ArgumentParser
from datetime import datetime

from redmine.time_entry import TimeEntry
from redmine.errors import TimeEntryAddException

_sucess_message = u"""
    TimeEntry successfully created with id {0}
    In project:         {1}
    In issue (id):      {2}
    For user:           {3}
    Activity:           {4}
                """

_failure_message = u"""
    TimeEntry creation failed with code {0}
    Extra details: {1}"""


def _spent_time(issue, date, hours, activity_id, comment):
    te = TimeEntry(issue)
    try:
        response = te.add(date, hours, activity_id, comment)
        print _sucess_message.format(
            response['id'],
            response['project']['name'],
            response['issue']['id'],
            response['user']['name'],
            response['activity']['name']
        )
    except TimeEntryAddException as exc:
        print _failure_message.format(
            exc.code,
            exc.details
        )


def _main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--issue',
                        type=int, required=True, dest='issue',
                        help='Issue identifier, IE: 1234')
    parser.add_argument('-d', '--date', dest='date',
                        default=None,
                        help='The date the time was spent',
                        type=str)
    parser.add_argument('-c', '--comment',
                        dest='comment',
                        default='Develop work',
                        help='A comment IE: Fix picker bug')
    parser.add_argument('-t', '--time',
                        type=float, dest="time", required=True,
                        help='Time spent IE: 1; 0.1')
    parser.add_argument('-a', '--activity',
                        type=float, dest="activity_id",
                        default=None,
                        help='Activity id')

    args = parser.parse_args()

    date = None
    if args.date:
        try:
            date = _get_date(args.date)
        except Exception:
            print "Please, specify the date in format {0}".format(TimeEntry.DATE_FORMAT)
            exit(9)

    _spent_time(args.issue, date, args.time, args.activity_id, args.comment)


def _get_date(string):
    return datetime.strptime(string, TimeEntry.DATE_FORMAT)


if __name__ == '__main__':
    _main()
