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
import json
import shutil
import urllib2
import urlparse

from .errors import IssueError
from .setting import Setting


class Issue(object):

    SHOW_URL = 'issues/%s.json?include=attachments'
    CREATE_URL = 'issues.json'

    def __init__(self, issue=None, subject=None, attachments=None):
        self._issue = str(issue)
        self._subject = str(subject)
        self._attachments = attachments
        self._setting = Setting()

    def get(self):
        return json.loads(self._call(self._get_show_url()))

    def create(self):
        params = {'issue':
                 {'project_id': self._setting.get_project(),
                  'tracker_id': self._setting.get_tracker(),
                  'subject': self._subject,
                  'uploads': self._attachments}}
        response = self._call(self._get_create_url(),
                              json.dumps(params),
                              {'Content-Type': 'application/json'})
        return json.loads(response)

    def get_attachments(self, chunk):
        issue = self.get()
        attachments = sorted(issue['issue']['attachments'],
                             key=lambda a: a['created_on'])
        attachments.reverse()

        # make sure it has exactly what we asked for
        issue_path = self._get_issue_path()
        if os.path.exists(issue_path):
            shutil.rmtree(issue_path)
        os.makedirs(issue_path)

        for attachment in attachments[:chunk]:
            path = os.path.join(issue_path, attachment['filename'])
            with file(path, 'w') as dump:
                dump.write(self._call(attachment['content_url']))
            print 'Dumped %s from %s' % (path, attachment['content_url'])

    def _call(self, url, data=None, header={}):
        headers = {'X-Redmine-API-Key': self._setting.get_key()}
        headers = dict(headers.items() + header.items())
        req = urllib2.Request(url, data, headers)

        try:
            response = urllib2.urlopen(req)
        except Exception as err:
            raise IssueError(err)
        else:
            return response.read()

    def _get_show_url(self):
        return urlparse.urljoin(self._setting.get_host(),
                                self.SHOW_URL % self._issue)

    def _get_create_url(self):
        return urlparse.urljoin(self._setting.get_host(), self.CREATE_URL)

    def _get_issue_path(self):
        return os.path.join(self._setting.get_path(), self._issue)
