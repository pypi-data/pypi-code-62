import os

class Extractor:
    def __init__(self, path, src_path):
        self.path = path
        if not(os.path.exists(path)):
            os.makedirs(path)
        self.basename = "{count:08d}.{ext}"
        self.count = 0
        self.src_path = src_path
        self.src_img = open(src_path, "rb")
        self.extracted = []

    def extract(self, start, end, ext):
        self.count += 1
        fname = self.basename.format(count=self.count, ext=ext)
        with open(f"{self.path}/{fname}", "wb") as fd:
            self.src_img.seek(start)
            data = self.src_img.read(max(0, end - start))
            fd.write(data)
            self.extracted.append(f"{self.path}/{fname}")
