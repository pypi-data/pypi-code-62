class Provider:
    def __init__(self, path, bsize=512):
        self.fd = open(path, "rb")
        self.bsize = bsize

    def find(self, needles, start=0):
        # TODO: replace this very basic implementation for a better one
        fd, bsize = self.fd, self.bsize
        fd.seek(start)
        data = fd.read(bsize)
        while data:
            if any(n for n in needles if n in data):
                for n in needles:
                    pos = data.find(n)
                    if pos > -1:
                        yield ((fd.tell() - bsize) // bsize, pos, n)
            data = fd.read(bsize)
