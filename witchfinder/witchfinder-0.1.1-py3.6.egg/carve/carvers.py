class Carver:
    def __init__(self, provider, extractor, formats):
        self.provider = provider
        self.extractor = extractor
        self.formats = formats

    def carve(self):
        needles = {}
        stack = {}
        for f in self.formats:
            needles.update({f.header: ("header", f), f.footer: ("footer", f)})
            stack[f] = {"header":[], "footer":[]}
        provider = self.provider
        extractor = self.extractor
        for block, offset, n in provider.find(needles):
            match_type, fmt = needles[n]
            stack[fmt][match_type].append((block, offset, n))
            if match_type == "footer":
                if stack[fmt]["footer"] and stack[fmt]["header"]:
                    end = stack[fmt]["footer"].pop()
                    start = stack[fmt]["header"].pop()
                else:
                    continue
                bsize = provider.bsize
                start = (start[0] * bsize) + start[1]
                end = (end[0] * bsize) + end[1] + len(n)
                extractor.extract(start, end, fmt.extension)