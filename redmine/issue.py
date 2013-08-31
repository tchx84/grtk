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

from setting import Setting


class Issue(object):

    ISSUE_URL = 'issues/%s.json?include=attachments'

    def __init__(self, issue):
        self._issue = str(issue)
        self._setting = Setting()

    def get_attachments(self, chunk):
        url = self._get_issue_url()
        issue_metadata = json.loads(self._request(url))
        attachments = sorted(issue_metadata['issue']['attachments'],
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
                dump.write(self._request(attachment['content_url']))
            print 'Dumped %s from %s' % (path, attachment['content_url'])

    def _request(self, url):
        headers = {'X-Redmine-API-Key': self._setting.get_key()}
        req = urllib2.Request(url, None, headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as err:
            raise LookupError('Could not retrieve %s (%s)' % (url, str(err)))
        else:
            return response.read()

    def _get_issue_url(self):
        return urlparse.urljoin(self._setting.get_host(),
                                self.ISSUE_URL % self._issue)

    def _get_issue_path(self):
        return os.path.join(self._setting.get_path(), self._issue)
