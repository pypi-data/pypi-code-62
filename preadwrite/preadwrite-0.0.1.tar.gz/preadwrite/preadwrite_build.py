import cffi

ffibuilder = cffi.FFI()
ffibuilder.set_source("_preadwrite", r"""
    #include <unistd.h>
""")  # <=

ffibuilder.cdef("""
    typedef long size_t;
    typedef long off_t;
    typedef long ssize_t;

    ssize_t pread(int fd, void *buf, size_t count, off_t offset);
    ssize_t pwrite(int fd, const void *buf, size_t count, off_t offset); 
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
