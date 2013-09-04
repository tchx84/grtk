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

from ConfigParser import ConfigParser


class Setting(object):

    GRTK_HOME = '.grtk/'

    def __init__(self):
        self._profile = 'default'
        self._home = os.path.expanduser("~")
        self._load_config()

    def _load_config(self):
        config_path = os.path.join(self._home, self.GRTK_HOME, 'config')
        config = ConfigParser()
        config.read(config_path)
        self._host = config.get(self._profile, 'host', '')
        self._key = config.get(self._profile, 'key', '')
        self._project = config.get(self._profile, 'project', None)
        self._tracker = config.get(self._profile, 'tracker', None)
        self._activity = config.get(self._profile, 'activity', None)

    def get_key(self):
        return self._key

    def get_path(self):
        return os.path.join(self._home, self.GRTK_HOME)

    def get_host(self):
        return self._host

    def get_project(self):
        return self._project

    def get_tracker(self):
        return self._tracker

    def get_activity(self):
        return self._activity
