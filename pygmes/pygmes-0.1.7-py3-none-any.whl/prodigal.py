import logging
import os
import subprocess
import re


class prodigal:
    def __init__(self, seq, outdir, ncores):
        self.seq = seq
        self.outdir = outdir
        self.logfile = os.path.join(outdir, "prodigal.log")
        if ncores == 1:
            logging.warning(
                "You are running Prodigal with a single core. This will be slow. We recommend using 4-8 cores."
            )
        self.faa = self.run(ncores)
        self.bed = self.make_bed()

    def run(self, cores=1):
        logging.debug("Launching prodigal now: %s" % self.seq)
        co = os.path.join(self.outdir, "genecoord.bgk")
        faa = os.path.join(self.outdir, "prot.faa")
        lst = ["prodigal", "-i", self.seq, "-p", "meta", "-o", co, "-a", faa]
        try:
            # do not rerun for now if we already attempted the training once
            if not os.path.exists(faa):
                with open(self.logfile, "w") as fout:
                    subprocess.run(" ".join(lst), cwd=self.outdir, check=True, shell=True, stdout=fout, stderr=fout)
            else:
                logging.debug("Prodigal output already exists")
        except Exception:
            logging.warning("Prodigal failed on this bin")
        return faa

    def make_bed(self):
        # parser for rpodigals faa using header information
        bedpath = os.path.join(self.outdir, "prot.bed")
        reg = re.compile(r"([\w\d.\-\+]+)_[0-9]+")
        with open(self.faa) as fin, open(bedpath, "w") as fout:
            for line in fin:
                if not line.startswith(">"):
                    continue
                column_char = " # "
                *_, start, stop, strandinfo, metadata = header.split(column_char)
                seq_name = column_char.join(_)[1:]

                m = reg.match(seq_name)
                if m is not None:
                    chrom = m.group(1)
                else:
                    logging.warning(
                        "Could not extract chromsome name from protein header. This is a bug in pygmes. Please report this on our github."
                    )
                    exit(1)

                if strandinfo == "1":
                    strand = "+"
                elif strandinfo == "-1":
                    strand = "-"
                else:
                    strand = "."

                newline = "{}\t{}\t{}\t{}\t{}\n".format(chrom, start, stop, strand, name)
                fout.write(newline)

        return bedpath

    def check_success(self):
        if os.stat(self.faa).st_size == 0:
            return False
        if not os.path.exists(self.faa):
            return False
        return True
