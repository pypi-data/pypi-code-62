from _preadwrite import ffi, lib


def pread(fd, n, offset):
    """
    Read at most n bytes from file descriptor fd at a position of offset, leaving the file offset unchanged.
    Return a bytestring containing the bytes read. If the end of the file referred to by fd has been reached,
    an empty bytes object is returned.

    Availability: Unix.
    """
    buf = ffi.new('unsigned char buf[]', n)
    read_bytes = lib.pread(fd, buf, n, offset)
    if read_bytes == -1:
        raise OSError(ffi.errno, "pread failed.")
    else:
        return ffi.buffer(buf, read_bytes)


def pwrite(fd, str, offset):
    """
    Write the bytestring in str to file descriptor fd at position of offset, leaving the file offset unchanged.
    Return the number of bytes actually written.

    Availability: Unix.
    """
    written_bytes = lib.pwrite(fd, str, len(str), offset)
    if written_bytes == -1:
        raise OSError(ffi.errno, "pwrite failed.")
    else:
        return written_bytes
