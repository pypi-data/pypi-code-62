#!/usr/bin/python3

r"""
Split up a file and yield its pieces based on some line terminator.

Usage looks like:
    $ /usr/local/cpython-3.6/bin/python3
    Python 3.6.0 (default, Apr 22 2017, 09:17:19)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import readline0
    >>> file_ = open('/etc/shells', 'r')
    >>> for line in readline0.readline0(file_=file_, separator=b'\n'):
    ...     print(line)
    ...
    b'# /etc/shells: valid login shells'
    b'/bin/sh'
    b'/bin/dash'
    b'/bin/bash'
    b'/bin/rbash'
    >>>

Of course separator need not be a newline; it defaults to a null byte.
"""

# This software is the proprietary property of The Regents of the University of California ("The Regents") Copyright (c)
# 1993-2006 The Regents of the University of California, Irvine campus. All Rights Reserved.

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.

# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.

# Neither the name of The Regents nor the names of its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.

# The end-user understands that the program was developed for research purposes and is advised not to rely exclusively
# on the program for any reason.

# THE SOFTWARE PROVIDED IS ON AN "AS IS" BASIS, AND THE REGENTS AND CONTRIBUTORS HAVE NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS. THE REGENTS AND CONTRIBUTORS SPECIFICALLY DISCLAIM ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES, INCLUDING BUT NOT LIMITED TO PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES, LOSE OF USE, DATA OR PROFITS, OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND UNDER ANY
# THEORY OF LIABILITY WHETHER IN CONTRACT, STRICT LIABILITY OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import re
import sys


def readline0(file_=sys.stdin, separator=b'\0', blocksize=2 ** 16):
    # pylint: disable=W1401
    # W1401: We really do want a null byte
    """
    Instantiate Readline0 class and yield what we get back.

    file_ defaults to sys.stdin, separator defaults to a null, and blocksize defaults to 64K.
    """
    if hasattr(file_, 'buffer'):
        # Do bytes I/O
        file_ = getattr(file_, 'buffer')
    readline0_obj = Readline0(file_, separator, blocksize)
    for line in readline0_obj.sequence():
        yield line


class Readline0(object):
    # pylint: disable=R0902
    # R0902: We really do need lots of instance attributes
    """Yield a series of blocks, separated by separator."""

    # This class assumes that there will be a null once in a while.  If you feed it with a huge block of data that has
    # no nulls (line separators), woe betide you.
    def __init__(self, file_, separator, blocksize):
        """Initialize."""
        self.file_ = file_
        self.blocksize = blocksize

        self.have_fraction = False
        self.fraction = None

        self.separator = separator

        self.fields = []

        self.yieldno = 0

        self.bang = b'!'
        self.metapattern = b'([^!]*)!|([^!]+)$'
        self.buffer_ = b''
        self.separator = separator

        # bytes objects have a split method, but it doesn't work, at least not in Python 3.1.2.  But the re module
        # works with bytes, so we use that.

        self.pattern = re.sub(self.bang, self.separator, self.metapattern)

        self.at_eof = False

    @classmethod
    def handle_field_pairs(cls, field_pairs):
        """Pick apart the pairs from our regex split and return the correct values."""
        regular_fields = []
        have_fraction = False
        fraction = None

        for field_pair in field_pairs:
            if field_pair[0]:
                if field_pair[1]:
                    # They're both not zero length - that's an error
                    raise AssertionError('Both field_pair[0] and field_pair[1] are non-empty')
                else:
                    # The first is not zero length, the second is zero length
                    regular_fields.append(field_pair[0])
            else:
                if field_pair[1]:
                    # the first is zero length, the second is not zero length
                    if have_fraction:
                        raise AssertionError('Already have a fraction')
                    fraction = field_pair[1]
                    have_fraction = True
                else:
                    # they're both zero length - this is legal for !! - yield one or the other but not both
                    assert field_pair[0] == field_pair[1]
                    regular_fields.append(field_pair[0])

        return regular_fields, have_fraction, fraction

    def get_fields(self):
        """Read a block, chop it up into fields - taking into account any leftover partial field."""
        if isinstance(self.file_, int):
            tail_block = os.read(self.file_, self.blocksize)
        else:
            # assume we have a file-like object
            tail_block = self.file_.read(self.blocksize)

        if tail_block:
            self.at_eof = False
        else:
            self.at_eof = True

        if self.have_fraction:
            block = self.fraction + tail_block
            self.fraction = None
            self.have_fraction = False
        else:
            block = tail_block

        field_pairs = re.findall(self.pattern, block)
        regular_fields, self.have_fraction, self.fraction = self.handle_field_pairs(field_pairs)

        # we put the fields in reverse order so we can repeatedly pop efficiently
        regular_fields.reverse()

        self.fields = regular_fields

    def sequence(self):
        """Generate each field (line) in turn."""
        while True:
            if not self.fields:
                self.get_fields()
            while self.fields:
                yield self.fields.pop()
            if self.at_eof:
                if self.have_fraction:
                    yield self.fraction
                break
