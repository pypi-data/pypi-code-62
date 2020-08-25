class FileFormat:
    def __init__(self, extension=None, header=None, footer=None, comment=None,
                 maxlen=None, minlen=None,
                 ):
        self.extension   = extension
        self.header      = header
        self.footer      = footer
        self.comment     = comment
        self.maxlen      = maxlen
        self.minlen      = minlen
    
    def __repr__(self):
        return (
            f"FileFormat(ext='{self.extension}', header={self.header}, footer='{self.footer}, "
            f"maxlen={self.maxlen}, minlen={self.minlen})"
            #f"\nComment: {self.comment}" * bool(self.comment)
        )
