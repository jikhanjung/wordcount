#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jikhanjung'

import codecs

filepath = 'test2.txt'
f = codecs.open(filepath, encoding='utf-8')
#f = open(filepath, 'r')
textdata = f.read()
f.close()

ignore_blank_line = False
#print textdata
col_count = 0
row_count = 0
page_count = 0
import string
import math
#print string.punctuation
col_per_row = 20
row_per_page = 10


import string
import math

ADD_SUCCESS = True
ADD_FAILURE = False

class wgj_char:
    def __init__(self):
        self.is_full = False
        self.half_full = False
        self.char_list = []
    def add_char(self, c):
        #print c,
        # half character
        if c.isalnum() and ord(c)<128 and c not in string.punctuation:
            #print "{"+c+"}",
            if self.is_full:
                #print "full"
                return ADD_FAILURE
            if self.half_full:
                self.half_full = False
                self.is_full = True
            else:
                self.half_full = True
                self.is_full = False
            self.char_list.append(c)
        else:
            #print "_"+c+"_",
            if self.half_full:
                #print "f"
                return ADD_FAILURE
            self.char_list.append(c)
            self.is_full = True
            self.half_full = False
        return ADD_SUCCESS
    def output(self):
        l = self.char_list
        if len(l)==1 and ord(l[0]) <128: l.append(' ')
        return "["+"".join(l)+"]"

class wgj_row:

    def __init__(self):
        self.char_per_row = 20
        self.char_list = []
        self.char_list.append( wgj_char() )
        self.is_full = False

    def add_char(self,c):
        curr_char = self.char_list[-1]
        rv = curr_char.add_char(c)
        #print curr_char.output()
        if rv == ADD_SUCCESS:
            #print "*S*",
            if curr_char.is_full:
                #print "*F*",
                curr_char = wgj_char()
                self.char_list.append(curr_char)
        else:
            curr_char = wgj_char()
            self.char_list.append(curr_char)
            rv = curr_char.add_char(c)
            if rv == ADD_SUCCESS:
                #print "*S*",
                if curr_char.is_full:
                    #print "*F*",
                    curr_char = wgj_char()
                    self.char_list.append(curr_char)

        if len( self.char_list )-1 >= self.char_per_row :
            self.is_full = True

        return ADD_SUCCESS
    def output(self):
        self.char_list.pop()
        char_list = [ c.output() for c in self.char_list ]
        return " ".join(char_list)

class wgj_page:
    def __init__(self):
        self.row_per_page = 10
        self.row_list = []
        self.row_list.append( wgj_row() )
        self.is_full = False

    def add_char(self,c):
        curr_row = self.row_list[-1]
        #print c,
        rv = curr_row.add_char(c)
        if rv == ADD_SUCCESS:
            if curr_row.is_full:
                curr_row = wgj_row()
                self.row_list.append(curr_row)
        else:
            curr_row = wgj_row()
            self.row_list.append(curr_row)
            curr_row.add_char(c)
            if curr_row.is_full:
                curr_row = wgj_row()
                self.row_list.append(curr_row)
        if len( self.row_list )-1 >= self.row_per_page :
            self.is_full = True

        return ADD_SUCCESS
    def new_line(self):
        curr_row = wgj_row()
        self.row_list.append( curr_row )
    def output(self):
        row_list = [ c.output() for c in self.row_list ]
        return "\n".join( row_list )

class Wongoji:

    def __init__(self):
        self.page_list = []
        self.ignore_blank_line = True
        self.page_list.append( wgj_page() )

    def add_text(self, text):
        curr_page = self.page_list[-1]
        for line in text.split('\n'):
            line.strip()
            if self.ignore_blank_line and line == "":
                continue

            for c in line:
                rv = curr_page.add_char(c)
                if rv == ADD_SUCCESS:
                    if curr_page.is_full:
                        curr_page = wgj_page()
                        self.page_list.append(curr_page)
                else:
                    curr_page = wgj_page()
                    self.page_list.append( curr_page )
                    curr_page.add_char(c)
                    if curr_page.is_full:
                        curr_page = wgj_page()
                        self.page_list.append(curr_page)
            curr_page.new_line()
    def output(self):
        i=1
        for page in self.page_list:
            print i, page.output()
            i+= 1
wgj = Wongoji()

wgj.add_text( textdata )

wgj.output()

print len( wgj.page_list[0].row_list )

print "hello"