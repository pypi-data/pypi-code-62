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

# these are all kinda inappropriate for pytest patterns
# pylint: disable=old-style-class, no-init, protected-access, no-self-use, unused-argument

"""Tests for the Fedora classes."""

from __future__ import unicode_literals
from __future__ import print_function

# external imports
import mock

# 'internal' imports
from resultsdb_conventions.fedoracoreos import FedoraCoreOSImageResult


class TestFedoraCoreOS:
    """Fedora CoreOS class tests."""

    def test_fedoracoreos_image_basic(self):
        """This is just a pretty basic overall test that instantiates
        the most complex class, produces a result and checks its
        properties.
        """
        res = FedoraCoreOSImageResult(
            platform='metal',
            filename='fedora-coreos-32.20200824.1.0-live.x86_64.iso',
            form='iso',
            arch='x86_64',
            build='32.20200824.1.0',
            stream='next',
            outcome='PASSED',
            tc_name='fcosbuild.some.test',
            note='note here',
            ref_url='https://www.job.link/',
            tc_url='https://www.test.case/',
            source='testsource' 
        )
        # Report to a MagicMock, so we can check create_result args
        fakeapi = mock.MagicMock()
        res.report(fakeapi)

        # basic attribute checks
        assert res.outcome == 'PASSED'
        assert res.tc_name == 'fcosbuild.some.test'
        assert res.note == 'note here'
        assert res.ref_url == 'https://www.job.link/'
        assert res.tc_url == 'https://www.test.case/'
        assert res.source == 'testsource'

        # check the testcase object
        assert res.testcase_object == {
            'name': 'fcosbuild.some.test',
            'ref_url': 'https://www.test.case/',
        }

        # check the extradata
        assert res.extradata == {
            'item': 'fedora-coreos-32.20200824.1.0-live.x86_64.iso',
            'meta.conventions': 'result fedoracoreos.build fedoracoreos.image',
            'fedoracoreos.build.version': '32.20200824.1.0',
            'fedoracoreos.build.stream': 'next',
            'fedoracoreos.image.arch': 'x86_64',
            'fedoracoreos.image.format': 'iso',
            'fedoracoreos.image.platform': 'metal',
            'source': 'testsource',
            'type': 'fcosbuild'
        }

        # check the groups
        assert res.groups == [
            {
                'description': 'source.testsource',
                'uuid': 'ddf8c194-5e34-50ec-b0e8-205c63b0dfc1'
            },
            {
                'description': 'fcosbuild.32.20200824.1.0',
                'uuid': '78d4cde6-2c7d-5562-b8bd-6fad3f7e5fa9'
            },
            {
                'description': 'testsource.32.20200824.1.0',
                'uuid': 'b1335dd9-91dd-504d-b8eb-c81382b08bb9'
            },
            {
                'description': 'image.fedoracoreos.metal.iso.x86_64',
                'uuid': '98072b18-3e22-5661-b834-cab0d8dda886'
            },
            {
                'description': 'testsource.fedoracoreos.metal.iso.x86_64',
                'uuid': '930d5d12-2b5b-5a5d-8b0d-7a056be19b28'
            }
        ]

# vim: set textwidth=120 ts=8 et sw=4:
