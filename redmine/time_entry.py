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

import json
import urllib
import urllib2
import urlparse
import datetime

from .setting import Setting
from .errors import TimeEntryAddException


class TimeEntry(object):

    DATE_FORMAT = '%Y-%m-%d'
    GET_URL = 'time_entries/%s.json'
    GET_ALL_URL = 'time_entries.json'
    POST_URL = 'time_entries.json'

    def __init__(self, issue):
        self.issue = issue
        self._setting = Setting()

    def add(self, date, hours, activity_id, comment):
        if not activity_id:
            activity_id = self._setting.get_activity()
        if not date:
            now = datetime.datetime.now()
            date = now.strftime(self.DATE_FORMAT)
        data = {
            "time_entry[issue_id]": self.issue,
            "time_entry[spent_on]": date,
            "time_entry[hours]": str(hours),
            "time_entry[activity_id]": int(activity_id),
            "time_entry[comments]": str(comment)
        }
        return json.loads(self._post(data))['time_entry']

    def _post(self, data):
        url = self._get_full_post_url()
        headers = {
            'X-Redmine-API-Key': self._setting.get_key()
        }
        #headers['Content-Type'] = 'application/json'
        req = urllib2.Request(url, urllib.urlencode(data, False), headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as err:
            if err.code == 422:
                failed = json.loads(err.read())['errors']
                raise TimeEntryAddException(err.message, err.code, failed)
            else:
                raise TimeEntryAddException(err.message, err.code)
        else:
            return response.read()

    def _get_full_post_url(self):
        return urlparse.urljoin(self._setting.get_host(),
                                self.POST_URL)
