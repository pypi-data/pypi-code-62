"""
Reader functions for lime files
"""
# pylint: disable=C0303

__all__ = [
    "Reader",
]

import sys
import os
from array import array
from .lib import lib
from .status import check_status


class Reader:
    """
    Reader class for lime files.

    Example
    -------
    
    >>> reader = Reader("conf.lime")
    >>> records = list(reader)
    >>> records[0]
    {
      'offset': 144, 
      'nbytes': 258, 
      'lime_type': 'xlf-info', 
      'bytes_pad': 6, 
      'MB_flag': 1, 
      'ME_flag': 1, 
      'data': '...'
    }
    """

    __slots__ = ["filename", "_fp", "_reader", "max_bytes"]

    def __init__(self, filename, max_bytes=64000):
        """
        Reads the content of a lime file
        
        Parameters
        ----------
        filename: str
           Name of the file
        max_bytes: int
           Max length of records to be read in directly.
           If larger, the data inside the record is not read.
        """
        assert os.path.isfile(filename)
        self.filename = os.path.abspath(filename)
        self.max_bytes = max_bytes
        self._fp = None
        self._reader = None

    def __del__(self):
        if self.isopen:
            self.close()

    @property
    def reader(self):
        "The c-lime reader"
        if not self.isopen:
            self.open()
        return self._reader

    @property
    def record(self):
        "Content of the current record"
        record = dict(
            offset=self.reader.rec_start,
            nbytes=lib.limeReaderBytes(self.reader),
            lime_type=lib.limeReaderType(self.reader),
            bytes_pad=lib.limeReaderPadBytes(self.reader),
            MB_flag=lib.limeReaderMBFlag(self.reader),
            ME_flag=lib.limeReaderMEFlag(self.reader),
        )

        if record["nbytes"] <= self.max_bytes:
            nbytes = record["nbytes"]
            arr = array("u", ["\0"] * nbytes)
            read_bytes = array("L", [nbytes])
            check_status(lib.limeReaderReadData(arr, read_bytes, self.reader))
            try:
                record["data"] = bytes(arr).decode().strip("\0")
            except UnicodeDecodeError:
                record["data"] = bytes(arr)

        return record

    @property
    def isopen(self):
        "Returns if the file is open"
        return self._reader is not None

    def open(self):
        "Opens the file reader"
        self._fp = lib.fopen(self.filename, "r")
        self._reader = lib.limeCreateReader(self._fp)

    def next(self):
        "Moves to the next record"
        if not self.isopen:
            raise RuntimeError("File needs to be open first")

        status = lib.limeReaderNextRecord(self.reader)
        if status != lib.LIME_EOF:
            check_status(status)
            return self.record
        raise StopIteration

    def close(self):
        "Closes the file reader"
        if not self.isopen:
            raise RuntimeError("File needs to be open first")

        lib.limeDestroyReader(self._reader)
        lib.fclose(self._fp)
        self._fp = None
        self._reader = None

    def __enter__(self):
        if self._reader is not None:
            self.close()
        self.open()
        return self

    def __exit__(self, typ, value, trb):
        self.close()

    def __len__(self):
        offset = lib.limeGetReaderPointer(self.reader)
        check_status(lib.limeSetReaderPointer(self.reader, 0))
        count = 0
        status = lib.limeReaderNextRecord(self.reader)
        while status != lib.LIME_EOF:
            check_status(status)
            status = lib.limeReaderNextRecord(self.reader)
            count += 1
        check_status(lib.limeSetReaderPointer(self.reader, offset))
        return count

    def __iter__(self):
        check_status(lib.limeSetReaderPointer(self.reader, 0))
        return self

    def __next__(self):
        return self.next()

    def __str__(self):
        rec = 0
        msg = 0
        first = True
        res = ""
        for record in self:
            if not first:
                res += "\n\n"
            if record["MB_flag"] == 1 or first:
                rec = 0
                msg += 1
                first = False
            rec += 1
            res += "Message:        %s\n" % msg
            res += "Record:         %s\n" % rec
            res += "Type:           %s\n" % record["lime_type"]
            res += "Data Length:    %s\n" % record["nbytes"]
            res += "Padding Length: %s\n" % record["bytes_pad"]
            res += "MB flag:        %s\n" % record["MB_flag"]
            res += "ME flag:        %s\n" % record["ME_flag"]
            if "data" not in record:
                res += "Data:           [Long record skipped]\n"
            elif isinstance(record["data"], str):
                res += 'Data:           "%s"\n' % record["data"]
            else:
                res += "Data:           [Binary data]\n"
        return res


def main():
    "Corresponding executable to lime_contents"
    assert len(sys.argv) == 2, "Usage: %s <lime_file>" % sys.argv[0]
    return str(Reader(sys.argv[1]))
