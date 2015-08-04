# -*- coding: utf-8 -*-
import sqlite3
import chardet
import re
from microsofttranslator import Translator
import time
import random
import traceback
import sys

# translator = Translator('soutasekine', 'Tk8KK3j2+W4f6v/n1lgXeLwsbZHVUdTnZLu3L++XNQI=')
# translator = Translator('skeven', 'vizaHdZEjZkP0ZdL/B3CQ0UO9yzsgmTT2hDtuvJFdL0=')
# translator = Translator('takikosekine', 'zjTibYqktK1UpZd2bepNVLflJlVCcSxjrtrmFJNwCWY=')
# translator = Translator('naosekine', 'M04ecskst3RZtaLpLZK4EbOG836TQf6r0IX7rmo5XKg=')
translator = Translator('ssekine', 'J27sphE2O9LiOcyTEya0ZDeesIpKjfDYIges9t5bFGY=')


def isNewWord(word, cur):
        word = (word,)
        cur.execute("SELECT from_word FROM wordTable WHERE from_word=?", word)
        if cur.fetchone():
            return False
        else:
            return True
def mainmethod():
	con = sqlite3.connect("wordBank_en_ja.db")
	cur = con.cursor()
	# cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")

	tocon = sqlite3.connect("wordBank_en_ch.db")
	tocur = tocon.cursor()
	try:
		tocur.execute("""CREATE TABLE wordTable(from_language text, from_word text, count integer, to_language text, to_word text);""")
	except Exception, e:
		print 'Target Table already exist'
		pass
	argvs = sys.argv
	# headword = "a"
	headword = argvs[1]
	cur.execute("SELECT from_word, count FROM wordTable WHERE from_word like \'" + headword + "%\'")
	for d in cur.fetchall():
		# print d[0]
		try:
			from_word = d[0]
			isNew = isNewWord(from_word,tocur)
			if isNew == True:
				to_word = translator.translate(from_word, 'zh-CHS')
				from_language = 'eng'
				to_language = 'zh-CHS'
				count = d[1]
				insertwordline = (from_language, from_word, count, to_language, to_word)

				tocur.execute("INSERT INTO wordTable(from_language, from_word, count, to_language, to_word) VALUES (?, ?, ?, ?, ?)", insertwordline)
				tocon.commit()
				print insertwordline
				time.sleep(random.random())
			else:
				print 'ALREADY EXIST'
		except Exception, e:
			print traceback.format_exc()
			pass

	tocon.close()
	con.close()
if __name__ == '__main__':
	while True:
		try:
			mainmethod()
		except Exception, e:
			print traceback.format_exc()
			pass