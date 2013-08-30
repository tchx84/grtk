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

from redmine.issue import Issue


def _fetch_patches(id, chunk):
    issue = Issue(id)
    try:
        issue.get_attachments(chunk)
    except Exception as err:
        print 'Stopped suddently: %s' % str(err)


def _main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--issue',
                        type=int, required=True, dest="issue",
                        help='Issue identifier, IE: 1234')
    parser.add_argument('-c', '--chunk',
                        type=int, dest="chunk", default=sys.maxint,
                        help='Fetch the last CHUNK patches, IE: 3')
    args = parser.parse_args()
    _fetch_patches(args.issue, args.chunk)

if __name__ == '__main__':
    _main()
