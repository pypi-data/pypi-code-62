'''pdf_rules

A framework to turn a pdf into a csv

'''

import os
import sys
import csv
import re
import inspect
import mimetypes
import listify as lstfy
import pdftotext as p2t
import collections.abc



class PDF:
    ''' PDF

    The PDF class holds the file contents and the rules used to
    later create a csv with the class CSV.


    Load a pdf, txt file or string into PDF

        pdf = PDF('path/to/file')
        print(pdf)



    pdf.add_level

    Add a level to the pdf to define 'tables'. A table can be
    any part of the pdf which occurs more than once and inherits
    data from 'higher' tables.


        an example would be

        ___ invoice.pdf ______________________________


            Account Number:     123456


            Charges:
                Foo     £50
                Bar     £5
                Baz     £0.5

            Total:      £55.5

        ______________________________________________


        Here, the charges; foo, Bar and Baz, can be
        read from the pdf as the rows of the csv.


        ___ invoice.csv _____________________


            +---------------------------+
            | account | charge | amount |
            +---------+--------+--------+
            | 123456  |  Foo   | £50    |
            +---------+--------+--------+
            | 123456  |  Bar   | £5     |
            +---------+--------+--------+
            | 123456  |  Baz   | £0.5   |
            +---------+--------+--------+


        _____________________________________


    The 'highest' table is the whole pdf, and therefore any
    tables created by the user inherit data that occurs once,
    or in the 'top level'.


    The PDF instance has 'levels' and 'fields', levels can be thought of
    as rows and fields as columns.


    To define a level, use pdf.add_level()

    To define a field, use pdf.add_field()


        '''

    def __init__(self, path):
        self.path = path
        try:
            mime = mimetypes.guess_type(path)
        except:
            mime = (None, None)

        if mime[0] == None:
            if isinstance(path, str):
                self.reader = self.str2lst()
                self.path = './'
            elif isinstance(path, list):
                self.reader = path
                self.path = './'
            else:
                raise TypeError('''
                Please pass a path or sting to PDF()
                You passed a %s
                        ''' % type(self.path))
        elif "pdf" in mime[0]:
            self.reader = self.pdf2lst()
        elif "text" in mime[0]:
            self.reader = self.txt2lst()
        else:
            try:
                self.reader = self.pdf2lst()
            except:
                self.reader = self.txt2lst()

        self.levels = {0: (
            lambda rd, i, l: i == 0,
            lambda rd, i, l: i == len(self.reader) - 1)}
        self.fields = {}
        self.hierarchy = {}

        self.process()


    def __str__(self):
        return '\n'.join([ str(i) + ' | ' + j
            for i, j in zip(range(len(self.reader)), self.reader) ])

    def __repr__(self):
        return str(self.reader)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n > len(self.reader):
            raise StopIteration
        self.n += 1
        return self.reader[self.n-1]

    def __len__(self):
        return len(self.reader)

    def __getitem__(self, key):
        return self.reader[key]

    def __add__(self, pdf):
        if isinstance(pdf, PDF):
            new = PDF(self.reader + pdf.reader)
            new.hierarchy = rec_update(self.hierarchy, pdf.hierarchy)
            new.levels = rec_update(self.levels, pdf.levels)
            new.process()
        elif isinstance(pdf, str):
            new = PDF(self.reader + pdf.split('\n'))
            new.hierarchy = self.hierarchy
            new.levels = self.levels
            new.process()
        elif isinstance(pdf, list):
            new = PDF(self.reader + pdf)
            new.hierarchy = self.hierarchy
            new.levels = self.levels
            new.process()
        else:
            raise TypeError('''
            Please add a string, list of strings or other PDF object
            You passed a %s
                    ''' % type(pdf))
        return new


#     def show_levels(self):
#         def line_in_tables(index, level=0):
#             if index in range(self.hierarchy[][0]['rows']):
#                 g
#             else:
#                 return False
#
#         for index, line in enumerate(reader):
#             t = line_in_tables(index)

    def add_level(self, trigger_start, trigger_end):
        n = len(self.levels.keys())
        self.levels[n] = (trigger_start, trigger_end)
        self.process()

    def add_field(self, name, trigger, rule, level=0):
        self.fields.setdefault(level, {})
        self.fields[level].update({name: (trigger, rule)})
        self.process()

    def process(self):
        def table_gen(l):
            p = l-1 if l > 0 else 0
            p_mt = max(self.hierarchy[p]) if l > 0 else 0
            p_min = self.hierarchy[p][0]['rows'][0] if l > 0 else 0
            p_max = (self.hierarchy[p][p_mt]['rows'][1] + 1 if l > 0
                    else len(self.reader) - 1)
            p_range = range(p_min, p_max)
            tab = [0, 0]

            trigger_start, trigger_end = self.levels[l]

            for index, line in enumerate(self.reader):
                last_t_end = tab[1]
                if not index in p_range or index < last_t_end:
                    continue
                try:
                    if trigger_start(self.reader, index, line):
                        tab = [index]
                        p_tab_end = p_max
                        for tbl in self.hierarchy[p]:
                            if index in range(
                                    self.hierarchy[p][tbl]['rows'][0],
                                    self.hierarchy[p][tbl]['rows'][1]):
                                p_tab_end = self.hierarchy[p][tbl]['rows'][1]

                        for i, ln in enumerate(self.reader):
                            if i < index:
                                continue
                            if i == p_tab_end:
                                tab = tab + [i]
                                yield tab
                                break

                            try:
                                if (trigger_end(self.reader, i, ln)
                                        and i > tab[0]):
                                    tab = tab + [i]
                                    yield tab
                                    break
                                elif (trigger_start(self.reader, i, ln)
                                        and i > index
                                        and i > tab[0]):
                                    tab = tab + [i]
                                    yield tab
                                    break
                            except IndexError:
                                pass

                        if tab == [index]:
                            tab = tab + [p_max]
                            yield tab

                except IndexError:
                    pass



        for l in self.levels:
            self.hierarchy[l] = {}
            for t_num, t in enumerate(table_gen(l)):
                self.hierarchy[l][t_num] = {'rows': t}

        tables = self.hierarchy.copy()

        for l in tables:
            for t in tables.get(l, {}):
                sr = tables[l][t]['rows'][0]
                er = tables[l][t]['rows'][1] + 1
                d = self.hierarchy[l][t].setdefault('data', {})
                for f in self.fields.get(l, {}):
                    trigger, rule = self.fields[l][f]
                    for index, line in enumerate(self.reader):
                        if not index in range(sr, er):
                            continue
                        if trigger(self.reader, index, line):
                            d[f] = rule(self.reader, index, line)
                            break
                    if not f in d.keys():
                        d[f] = None

    def pdf2lst(self):
        '''load a pdf file into reader'''
        l = []
        with open(self.path, 'rb') as fh:
            pdf = p2t.PDF(fh)
            for page in pdf:
                for line in page.split('\n'):
                    l.append(line)
        return l

    def txt2lst(self):
        '''load a plaintext file into reader'''
        l = []
        with open(self.path, 'r') as fh:
            for line in fh.readlines():
                l.append(line.replace('\n', ''))
        return l

    def str2lst(self):
        '''turn string into list of strings'''
        return self.path.split('\n')

    def write_reader(self):
        '''write reader to file'''
        with open(os.path.basename(self.path) + '.txt', 'w',
                encoding='utf-8') as fh_o:
            fh_o.write(self.__str__())



class CSV:
    '''populate a csv from rules and level structure'''
    def __init__(self, PDF):
        self.PDF = PDF
        rd = self.PDF.reader
        self.default_outpath = (
                os.path.splitext(self.PDF.path)[0]
                + '_pdfrules.csv')

        h = self.PDF.hierarchy.copy()

        self.header = [ f for f in [
                list(h[l][0].setdefault('data', {}))
                for l in list(h.keys()) ] ]
        self.header = [ item for sublist in self.header
                for item in sublist ]
        self.csv = [self.header]

        depth = max(h.keys())


        def segment(l, t):
            return [ h[l][t]['data'][d] for d
                    in h[l][t]['data'].keys() ]


        def parent_seg(l, t):
            yield segment(l, t)
            while l >= 0:
                if l == 0:
#                     yield segment(0, 0)
                    l -= 1
                    break
                else:
                    ts = h[l][t]['rows'][0]
                    te = h[l][t]['rows'][1]
                    for tbl in h[l-1]:
                        if (ts < h[l-1][tbl]['rows'][0]
                        or ts > h[l-1][tbl]['rows'][1]):
                            continue
                        if te <= h[l-1][tbl]['rows'][1]:
                            yield segment(l-1, tbl)
                            l -= 1
                            t = tbl
                            break
                        else:
                            raise IndexError('''
            level %s
            table %s does not fall in table %s on level %s
                                    ''' % (l, t, tbl, l-1))

        for t in h[depth]:
            line  = []
            for i in parent_seg(depth, t):
                line = i + line
            self.csv.append(line)

#         print(self.csv)



    def __len__(self):
        return len(self.csv)

    def __str__(self):
        return '\n' + '\n'.join(str(i) for i in self.csv)

    def __repr__(self):
        return str(self.csv)

    def __add__(self, csv):
        pass

    def __sub__(self, csv):
        pass

    def __mul__(self, num):
        pass

    def __lt__(self, csv):
        pass

    def __gt__(self, csv):
        pass

    def __le__(self, csv):
        pass

    def __ge__(self, csv):
        pass

    def __eq__(self, csv):
        pass

    def __neq__(self, csv):
        pass


    def write(self,
            path=None,
            encoding='utf-8'):
        if path == None:
            path = self.default_outpath
        with open(path, 'w', encoding=encoding) as fh:
            writer = csv.writer(fh, lineterminator='\n')
            for l in self.csv:
                writer.writerow(l)


def listify(l):
    '''turn line into list'''
    return re.sub('   *', '  ', l.lstrip()).split('  ')


def rec_update(d, d2):
    for k, v in d2.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = rec_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d



if __name__ == '__main__':
    l = '''         Invoice Number:     12345
                    Account Number:     1234567890
                    Monies: £££££

            table - AB12 3CD
                circuit1 - £50 - copper - start - end
                circuit2 - £100 - mobile - start - end
                            total - £150

            table - EF45 6GH
                circuit3 - £150 - LAN - start - end
                circuit4 - £200 - WAN - start - end
                            total - £350
                '''

    pdf = PDF(l)
    print(pdf)
    print()

    pdf.add_level(lambda rd, i, li: 'table' in li,
            lambda rd, i, li: 'total' in li)
    pdf.add_level(lambda rd, i, li: 'circuit' in li,
            lambda rd, i, li: 'circuit' in li)


    pdf.add_field('inv_num',
            trigger=lambda rd, i, l: 'Invoice Number' in l,
            rule=lambda rd, i, l: listify(l)[-1])
    pdf.add_field('acc_num',
            trigger=lambda rd, i, l: 'Account Number' in l,
            rule=lambda rd, i, l: listify(l)[-1])

    pdf.add_field('PC',
            trigger=lambda rd, i, l: False,#'table' in l,
            rule=lambda rd, i, l: l.split(' - ')[-1].strip(),
            level=1)

    pdf.add_field('charge',
            trigger=lambda rd, i, l: 'circuit' in l,
            rule=lambda rd, i, l: l.split(' - ')[1].strip(),
            level=2)


    print()
    for l in pdf.hierarchy.keys():
        print('pdf.level ' + str(l) + '\t' + str(pdf.hierarchy[l]))

    print()
    for l in pdf.fields.keys():
        for f in pdf.fields[l].keys():
            print('pdf.fields lvl ' + str(l) + ':\t' + str(f)
                    + '\n' + str(pdf.fields[l][f]))

    csv=CSV(pdf)
    print()
    print('csv:\t%s' % csv)



