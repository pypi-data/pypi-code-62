#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
RocketIsp calculates delivered Isp for liquid rocket thrust chambers.

<Paragraph description see docstrings at http://www.python.org/dev/peps/pep-0257/>
RocketIsp is a simplified JANNAF approach to calculating delivered
specific impulse (Isp) for a liquid rocket thrust chamber.


RocketIsp
Copyright (C) 2020  Applied Python

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os
here = os.path.abspath(os.path.dirname(__file__))


# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2020 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "4 - Beta" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

#
# import statements here. (built-in first, then 3rd party, then yours)
#
# Code goes below.
# Adjust docstrings to suite your taste/requirements.
#

class IspDelivered(object):
    """RocketIsp calculates delivered Isp for liquid rocket thrust chambers.

    Longer class information....
    Longer class information....

    Attributes::
    
        likes_spam: A boolean indicating if we like SPAM or not.

        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self):
        """Inits IspDelivered with blah."""
        self.likes_spam = True
        self.eggs = 3

    def public_method(self, arg1, arg2, mykey=True):
        """Performs operation blah.
        
        :param arg1: description of arg1
        :param arg2: description of arg2
        :type arg1: int
        :type arg2: float
        :keyword mykey: a needed input
        :type mykey: boolean
        :return: None
        :rtype: None
        
        .. seealso:: blabla see stuff
        
        .. note:: blabla noteworthy stuff
        
        .. warning:: blabla arg2 must be non-zero.
        
        .. todo:: blabla  lots to do
        """
        #  Answer to the Ultimate Question of Life, The Universe, and Everything
        return 42

if __name__ == '__main__':
    C = IspDelivered()
