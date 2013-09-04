#!/usr/bin/env python

# Copyright (c) 2013 Martin Abente Lahaye. - martin.abente.lahaye@gmail.com
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

import sys

from argparse import ArgumentParser

from redmine.attachment import Attachment
from redmine.issue import Issue
from redmine.errors import IssueError
from redmine.errors import AttachmentError

_success_message = u'''
    Issue successfully created with id {0}
    With subject:   {1}
    With tracker:   {2}
    In project:     {3}
                   '''

_failure_message = u'''
    Issue creation failed while {0}
    Stack details:  {1}
                   '''


def _send_attachments(paths):
    attachments = []
    for path in paths:
        attachment = Attachment()
        try:
            attachment.create(path)
        except AttachmentError as err:
            print _failure_message.format('creating attachment', err.message)
            sys.exit(-1)
        attachments.append({'token': attachment._token,
                            'filename': attachment._name,
                            'content_type': 'text/plain'})
    return attachments


def _create_issue(subject, attachments):
    issue = Issue(None, subject, attachments)
    try:
        metadata = issue.create()
        print _success_message.format(
            metadata['issue']['id'],
            metadata['issue']['subject'],
            metadata['issue']['tracker']['name'],
            metadata['issue']['project']['name'])
    except IssueError as err:
        print _failure_message.format('creating issue', err.message)
        sys.exit(-1)


def _main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--files', nargs='*',
                        type=str, required=True, dest="files",
                        help='list of patches to be sent, IE: 000*')
    parser.add_argument('-s', '--subject',
                        type=str, required=True, dest="subject",
                        help='issue subject, IE: \"New Feature\"')
    args = parser.parse_args()
    _create_issue(args.subject, _send_attachments(args.files))

if __name__ == '__main__':
    _main()
