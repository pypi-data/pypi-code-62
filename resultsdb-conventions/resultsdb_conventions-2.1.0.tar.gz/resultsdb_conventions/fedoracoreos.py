# Copyright (C) Red Hat Inc.
#
# resultsdb_conventions is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:   Adam Williamson <awilliam@redhat.com>

"""Fedora CoreOS-specific conventions."""

from __future__ import unicode_literals
from __future__ import print_function

# stdlib imports
import logging

# internal imports
from .base import Result

# pylint:disable=invalid-name
logger = logging.getLogger(__name__)


class FedoraCoreOSBuildResult(Result):
    """Result from a test of a Fedora CoreOS build in general (not
    related to a specific deliverable).
    """
    def __init__(self, build, stream, *args, **kwargs):
        self.build = build
        self.stream = stream
        super(FedoraCoreOSBuildResult, self).__init__(*args, **kwargs)
        # item is the build unless subclass overrides
        self.extradata.update({
            'item': self.build,
            'type': 'fcosbuild',
        })
        self.conventions.append('fedoracoreos.build')

    def default_extradata(self):
        """Add values from the metadata."""
        super(FedoraCoreOSBuildResult, self).default_extradata()
        extradata = {
            'fedoracoreos.build.version': self.build,
            'fedoracoreos.build.stream': self.stream,
        }
        extradata.update(self.extradata)
        self.extradata = extradata

    def default_groups(self):
        super(FedoraCoreOSBuildResult, self).default_groups()
        self.add_group('fcosbuild', self.build)
        if self.source:
            self.add_group(self.source, self.build)


class FedoraCoreOSImageResult(FedoraCoreOSBuildResult):
    """Result from testing a specific image from a Fedora CoreOS
    build. Values are mostly expected to come from the FCOS release
    JSON. platform is "metal", "aliyun", "aws" etc. filename is the
    filename of the image. form is the format (e.g. "iso", "tar.gz").
    arch is the architecture.
    """
    def __init__(self, platform, filename, form, arch, *args, **kwargs):
        self.platform = platform
        self.filename = filename
        self.format = form
        self.arch = arch
        super(FedoraCoreOSImageResult, self).__init__(*args, **kwargs)
        # when we have an image, item is always the filename
        self.extradata.update({
            'item': self.filename,
        })
        self.conventions.append('fedoracoreos.image')

    def default_extradata(self):
        """Populate extradata from image properties."""
        super(FedoraCoreOSImageResult, self).default_extradata()
        extradata = {
            'fedoracoreos.image.arch': self.arch,
            'fedoracoreos.image.format': self.format,
            'fedoracoreos.image.platform': self.platform,
        }
        extradata.update(self.extradata)
        self.extradata = extradata

    def default_groups(self):
        """Add to generic result groups for this image."""
        super(FedoraCoreOSImageResult, self).default_groups()
        imgid = "fedoracoreos.{0}.{1}.{2}".format(self.platform, self.format, self.arch)
        self.add_group('image', imgid)
        if self.source:
            # We cannot easily do a URL here, unless we start having
            # a store of 'known' sources and how URLs are built for
            # them, or using callbacks, or something. I think we might
            # just ask downstreams to get the group from the group
            # list and add the URL to it?
            self.add_group(self.source, imgid)

# vim: set textwidth=120 ts=8 et sw=4:
