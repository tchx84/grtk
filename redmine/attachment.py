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
import urlparse
import urllib2

from .errors import AttachmentError
from .setting import Setting


class Attachment(object):

    UPLOAD_URL = '/uploads.json'

    def __init__(self):
        self._token = None
        self._name = None
        self._setting = Setting()

    def create(self, path):
        url = self._get_attachment_url()
        data = None
        with file(path, 'rb') as source:
            data = source.read()

        metadata = json.loads(self._call(url, data))
        if 'upload' in metadata and 'token' in metadata['upload']:
            self._token = metadata['upload']['token']
            self._name = os.path.basename(path)
        else:
            raise AttachmentError('Token not found')

    def _call(self, url, data):
        headers = {'X-Redmine-API-Key': self._setting.get_key(),
                   'Content-Type': 'application/octet-stream'}

        req = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(req)
        except Exception as err:
            raise AttachmentError(err)
        else:
            return response.read()

    def _get_attachment_url(self):
        return urlparse.urljoin(self._setting.get_host(), self.UPLOAD_URL)
