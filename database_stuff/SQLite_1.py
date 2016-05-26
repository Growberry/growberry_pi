#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('test.db')

with con:

    cur = con.cursor()

    data = cur.execute(SELECT * FROM Cars;)