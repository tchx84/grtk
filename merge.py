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

import os
import sys
import subprocess
from argparse import ArgumentParser

from redmine.issue import Issue

_failure_message = u'''
    Could not merge patch set {0}
    Extra details: {1}
    Please try:
        $git checkout -b {2}
        $git git am {3} -s --3way
                    '''
_success_message = u'''
    Patch set {0} successfully merged
                   '''


def _merge_patches(issue):
    issue_path = issue._get_issue_path()
    patch_set = sorted([os.path.join(issue_path, p)
                       for p in os.listdir(issue_path)])
    patches = ' '.join(patch_set)

    try:
        _call('git checkout master')
        _call('git pull')
        _call('git checkout -b %s' % issue._issue, True)
        _call('git am %s' % patches, True)
    except Exception as err:
        _call('git am --abort')
        _call('git checkout master')
        _call('git branch -D %s' % issue._issue)
        print _failure_message.format(
            issue._issue, err, issue._issue, patches)
        sys.exit(-1)
    print _success_message.format(issue._issue)


def _call(cmd, safe=False):
    with open(os.devnull, "w") as fnull:
        if safe:
            subprocess.check_call(cmd, shell=True, stdout=fnull, stderr=fnull)
        else:
            subprocess.call(cmd, shell=True, stdout=fnull, stderr=fnull)


def _main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--issue',
                        type=int, required=True, dest="issue",
                        help='issue identifier, IE: #1234')
    args = parser.parse_args()

    issue = Issue(args.issue)
    _merge_patches(issue)

if __name__ == '__main__':
    _main()
