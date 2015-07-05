# -*- coding: utf-8 -*-
import sqlite3
import chardet
import traceback
import re
import string

# word = u'“em'
# word = string.replace(word, u'“', u'')
# word = string.replace(word, u'”', u'')
# word = string.replace(word, u'`', u'')
# word = string.replace(word, u'‘', u'')
# print word

# #target 2231
con = sqlite3.connect("wordBank.db")
cur = con.cursor()
cur.execute("SELECT from_language, from_word, count, to_language, to_word FROM wordTable;")
iterator = 0
for d in cur.fetchall():
	try:
		word = d[1]
		word = string.replace(word, u'“', u'')
		word = string.replace(word, u'”', u'')
		word = string.replace(word, u'`', u'')
		word = string.replace(word, u'‘', u'')
		cur.execute("UPDATE wordTable set from_word=? WHERE from_word=?", (word, d[1]))
		con.commit()
		print 'DONE %s' % iterator
		iterator = iterator + 1
	except:
		pass
con.close()
