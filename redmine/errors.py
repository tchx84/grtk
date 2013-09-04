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


class TimeEntryAddException(Exception):

    def __init__(self, message, code, details=None):
        Exception.__init__(self, message)
        self.message = message
        self.code = code
        self.details = details

    def __repr__(self):
        return '{0} [code: {1}: {2}'.format(
            self.message, self.code, self.details)


class IssueError(Exception):
    pass


class AttachmentError(Exception):
    pass
