# -*- coding: utf-8 -*-
import sqlite3
import chardet
import re
from microsofttranslator import Translator
import time
import random

translator = Translator('soutasekine', 'Tk8KK3j2+W4f6v/n1lgXeLwsbZHVUdTnZLu3L++XNQI=')
# translator = Translator('skeven', 'vizaHdZEjZkP0ZdL/B3CQ0UO9yzsgmTT2hDtuvJFdL0=')


def isNewWord(word, cur):
        word = (word,)
        cur.execute("SELECT from_word FROM wordTable WHERE from_word=?", word)
        if cur.fetchone():
            return False
        else:
            return True
def mainmethod():
	con = sqlite3.connect("wordBank_ita_jpn.db")
	cur = con.cursor()
	# cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")

	tocon = sqlite3.connect("wordBank_ita_eng.db")
	tocur = tocon.cursor()
	try:
		tocur.execute("""CREATE TABLE wordTable(from_language text, from_word text, count integer, to_language text, to_word text);""")
	except Exception, e:
		print 'Target Table already exist'
		pass

	cur.execute("SELECT from_word, count FROM wordTable")
	for d in cur.fetchall():

		from_word = d[0]
		isNew = isNewWord(from_word,tocur)
		if isNew == True:
			to_word = translator.translate(from_word, 'en')
			from_language = 'it'
			to_language = 'en'
			count = d[1]
			insertwordline = (from_language, from_word, count, to_language, to_word)

			tocur.execute("INSERT INTO wordTable(from_language, from_word, count, to_language, to_word) VALUES (?, ?, ?, ?, ?)", insertwordline)
			tocon.commit()
			print insertwordline
			time.sleep(random.random())
		else:
			print 'ALREADY EXIST'

	tocon.close()
	con.close()
if __name__ == '__main__':
	while True:
		try:
			mainmethod()
		except Exception, e:
			pass