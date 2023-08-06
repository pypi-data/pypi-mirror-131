#     pdf_rules
#     See LICENSE for copyright information

'''pdf_rules

A framework to turn a PDFs into a CSVs'''


import os
import sys
import csv
import re
import inspect
import mimetypes
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
    data from 'higher' tables. For example:

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

    To define a field, use pdf.add_field()'''

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
        if self.n >= len(self.reader):
            raise StopIteration
        l = self.reader[self.n]
        self.n += 1
        return l

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


    # TODO: unit tests for last_entry
    def last_entry(self, key):
        for l in self.hierarchy:
            if not key in self.hierarchy[l][0]['data']:
                continue
            t = len(self.hierarchy[l]) - 1
            while True:
                try:
                    return self.hierarchy[l][t]['data'][key]
                except:
                    t -= 1

    # TODO: finish show_levels method to illustrate hierarchy
    def show(self):
        try:
            import curses
        except ImportError:
            print("[-] can't use PDF.show, curses not installed", 
                    file=sys.stderr)
            return None

        stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

#        legend = curses.newwin(curses.LINES - 4, 0,
#                curses.COLS - 1, curses.LINES - 1)

        # define colours, default (0) is white on black.
        #   we want levels indicated by background colour
        #   triggers will be reversed italic
        #   strings found by rules will be reversed bold
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_YELLOW)

        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(11, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_WHITE)

        def del_type(l, rng):
            if not l - 1 in rng:
                return '\\'
            if not l + 1 in rng:
                return '/'
            else:
                return '|'

        def lin(l, rng, lvl):
            return '%s%s %s %s' % (l, '  ' * lvl, del_type(l, rng),
                    self.reader[l])

        def show_main(stdscr):
            x = 0
            y = 0

            while True:
                stdscr.clear()

                # write whole document in black & white
                for i, l in enumerate(self):
                    try:
                        stdscr.addstr(y + i, 0, ('%s | %s' % (i, l))[x:],
                                curses.color_pair(0))
                    except curses.error:
                        pass

                # re-write levels
                for lvl in self.hierarchy:
                    for tbl in self.hierarchy[lvl]:

                        rng = range(self.hierarchy[lvl][tbl]['rows'][0],
                                self.hierarchy[lvl][tbl]['rows'][1] + 1)

                        for l in rng:

                            # redraw with new background
                            try:
                                stdscr.addstr(y + l, 0,
                                        lin(l, rng, lvl)[x:],
                                        curses.color_pair(lvl))
                            except curses.error:
                                pass

                            # check for triggers
                            if lvl in self.fields.keys():
                                for f in self.fields[lvl]:
                                    if self.fields[lvl][f][0](self.reader, l,
                                            self.reader[l]):

                                        # make line num reversed
                                        try:
                                            stdscr.addstr(y + l, 0,
                                                    lin(l, rng,
                                                        lvl)[len(str(l))][x:],
                                                    curses.A_REVERSE)
                                        except curses.error:
                                            pass

                # ket key inputs
                stdscr.refresh()
                k = stdscr.getch()

                if k == curses.KEY_DOWN:
                    y -= 1
                if k == curses.KEY_UP and y < 0:
                    y += 1

                if k == curses.KEY_RIGHT:
                    x += 1
                elif k == curses.KEY_LEFT and x > 0:
                    x -= 1

                if k == ord('g'):
                    y = 0
                if k == ord('G'):
                    y = -len(self) + stdscr.getmaxyx()[0]
                if k == ord('q'):
                    break

        curses.wrapper(show_main)

        # show_main(stdscr)


    def add_level(self, trigger_start, trigger_end):
        '''add a new level to the pdf hierarchy

        :trigger_start: `lambda rd, i, l: <expression>`
                        where <expression>

        '''
        n = len(self.levels.keys())
        self.levels[n] = (trigger_start, trigger_end)
        self.process()

    def add_field(self, name, trigger, rule, level=0, fallback=None):
        '''add a data field to look for in a certain level'''
        self.fields.setdefault(level, {})
        self.fields[level].update({name: (trigger, rule, fallback)})
        self.process()

    def process(self):
        def table_gen(l):
            '''generate [table_start, table_end] for each table,
            yield them in the order we want them'''

            # calculate parent level num, last table num and range
            p = l-1 if l > 0 else 0
            p_mt = max(self.hierarchy[p]) if l > 0 else 0
            p_min = self.hierarchy[p][0]['rows'][0] if l > 0 else 0
            p_max = (self.hierarchy[p][p_mt]['rows'][1] + 1 if l > 0
                    else len(self.reader) - 1)
            p_range = range(p_min, p_max)
            tab = [0, 0]

            trigger_start, trigger_end = self.levels[l]

            # read the document, skip lines not included in parent table
            for index, line in enumerate(self.reader):
                last_t_end = tab[1]
                if not index in p_range or index < last_t_end:
                    continue

                # check output of trigger_start on each line
                try:

                    # triggered!
                    if trigger_start(self.reader, index, line):
                        tab = [index]
                        p_tab_end = p_max

                        # find where to stop reading this table
                        for tbl in self.hierarchy[p]:
                            if index in range(
                                    self.hierarchy[p][tbl]['rows'][0],
                                    self.hierarchy[p][tbl]['rows'][1]):
                                p_tab_end = self.hierarchy[p][tbl]['rows'][1]

                        # read newly found table in separate loop
                        for i, ln in enumerate(self.reader):
                            if i < index:
                                continue

                            # no trigger_end, table end same as parent
                            if i == p_tab_end:
                                tab = tab + [i]
                                yield tab
                                break

                            try:
                                # triggered! yield complete table and break
                                if (trigger_end(self.reader, i, ln)
                                        and i >= tab[0]):
                                    tab = tab + [i]
                                    yield tab
                                    break
                                elif (trigger_start(self.reader, i, ln)
                                        and i > index
                                        and i > tab[0]):
                                    tab = tab + [i-1]
                                    yield tab
                                    break

                            # allow trigger_end to read next line when it throws exception
                            except IndexError:
                                pass

                        # if trigger_end not triggered,
                        # last row of table = last row of parent
                        if tab == [index]:
                            tab = tab + [p_max]
                            yield tab

                # allow IndexErrors to pass by, these happen if
                # trigger_start called with rd[i+1] (for example)
                except IndexError:
                    pass


        # create hierarchy tree, add table rows
        for l in self.levels:
            self.hierarchy[l] = {}
            for t_num, t in enumerate(table_gen(l)):
                self.hierarchy[l][t_num] = {'rows': t}

        # we can't change the dictionary we loop over, so read a copy
        tables = self.hierarchy.copy()

        # for each level, read through that level's tables
        for l in tables:
            for t in tables.get(l, {}):
                sr = tables[l][t]['rows'][0]
                er = tables[l][t]['rows'][1] + 1
                d = self.hierarchy[l][t].setdefault('data', {})

                # read each table looking for triggers
                for f in self.fields.get(l, {}):
                    trigger, rule, fallback = self.fields[l][f]
                    for index, line in enumerate(self.reader):
                        if not index in range(sr, er):
                            continue

                        try:
                            # triggered! get result of rule function
                            if trigger(self.reader, index, line):
                                try:
                                    d[f] = rule(self.reader, index, line)
                                except:
                                    d[f] = None
                                if d[f] == None and fallback != None:
                                    d[f] = fallback
                                break
                        except IndexError:
                            pass

                    # add fallback if not triggered
                    if not f in d.keys():
                        d[f] = fallback

    def pdf2lst(self):
        '''load a pdf file into reader'''
        import pdftotext as p2t
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
    def __init__(self, pdf: PDF):

        # allows creation of null CSV by passing None as arg
        if pdf == None:
            pdf = PDF('')
            pdf.path = ''
            pdf.hierarchy = {}
            pdf.header = ''

        self.pdf = pdf
        self.default_outpath = (
                os.path.splitext(self.pdf.path)[0]
                + '_pdfrules.csv')

        h = self.pdf.hierarchy.copy()

        self.header = [ f for f in [
                list(h[l][0].setdefault('data', {}))
                for l in list(h.keys()) ] ]
        self.header = [ item for sublist in self.header
                for item in sublist ]
        self.csv = [self.header]

        try:
            depth = max(h.keys())
        except ValueError:
            # in case null CSV being created
            return


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

    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        if self.n < len(self.csv):
            l = self.csv[self.n]
            self.n += 1
            return l
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self.csv[item]

    def __setitem__(self, i, elem):
        self.csv[i] = elem

    def __str__(self):
        return '\n' + '\n'.join(str(i) for i in self.csv)

    def __repr__(self):
        return str(self.csv)

    def __add__(self, csv2):
        if isinstance(csv2, CSV) or isinstance(csv2, list):
            for l in csv2:
                self.csv.append(l)
            return self
        else:
            raise TypeError('''
        The CSV object does not support adding %s objects'''
        % type(csv2))

    def __sub__(self, csv2):
        if isinstance(csv2, CSV):
            for l in csv2:
                if l in self.csv:
                    self.csv.remove(l)
            return self
        elif isinstance(csv2, list):
            if isinstance(csv2[0], list):
                for l in csv2:
                    if l in self.csv:
                        self.csv.remove(l)
                return self
            else:
                if csv2 in self.csv:
                    self.csv.remove(csv2)
                    return self
                else:
                    return self
        else:
            raise TypeError('''
        The CSV object does not support subtractiong %s objects'''
        % type(csv2))

    def __eq__(self, csv2):
        if isinstance(csv2, CSV):
            return self.csv == csv2.csv
        else:
            return self.csv == csv2

    def __neq__(self, csv2):
        if isinstance(csv2, CSV):
            return self.csv != csv2.csv
        else:
            return self.csv != csv2


    def update_header(self, csv2):
        if isinstance(csv2, CSV):
            self.csv[0] = csv2[0]
        elif isinstance(csv2, list):
            self.csv[0] = csv2
        else:
            raise TypeError('''
        CSV.update_header() takes a list or another CSV''')

    def insert_column(self, field: str, data):
        '''add an new column to the csv, data will be appended
        if iterable, otherwse duplicated'''
        if not isinstance(data, list):
            self.csv[0].append(field)
            for i in range(1, len(self.csv)):
                self.csv[i].append(data)
        else:
            self.csv[0].append(field)
            for i in range(1, len(data)):
                self.csv[i].append(data[i])

    def write(self, path=None, encoding='utf-8'):
        if path == None:
            path = self.default_outpath
        with open(path, 'w', encoding=encoding) as fh:
            writer = csv.writer(fh, lineterminator='\n')
            for l in self.csv:
                writer.writerow(l)


def listify(l):
    '''turn line into list, delimited by >1 space'''
    return re.sub('   *', '  ', l.lstrip()).split('  ')


def rec_update(d, d2):
    for k, v in d2.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = rec_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

