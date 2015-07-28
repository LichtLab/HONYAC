# -*- coding: utf-8 -*-
import sqlite3
import chardet
import re


def isNewWord(word, cur):
        word = (word,)
        cur.execute("SELECT from_word FROM wordTable WHERE from_word=?", word)
        if cur.fetchone():
            return False
        else:
            return True
def mainmethod():
	con = sqlite3.connect("wordBank_spa_jpn.db")
	cur = con.cursor()
	try:
		cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")
	except Exception, e:
		print 'INDEX ALREADY'
	# cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")

	tocon = sqlite3.connect("wordBank_spa_jpn_clean.db")
	tocur = tocon.cursor()
	try:
		tocur.execute("""CREATE TABLE wordTable(from_language text, from_word text, count integer, to_language text, to_word text);""")
	except Exception, e:
		print 'Target Table already exist'
		pass

	cur.execute("SELECT from_word,to_language, count FROM wordTable")
	for d in cur.fetchall():

		from_word = d[0]
		isNew = isNewWord(from_word,tocur)
		if isNew == True:
			to_word = d[1]
			from_language = 'spa/por'
			to_language = 'ja'
			count = d[2]
			insertwordline = (from_language, from_word, count, to_language, to_word)

			tocur.execute("INSERT INTO wordTable(from_language, from_word, count, to_language, to_word) VALUES (?, ?, ?, ?, ?)", insertwordline)
			tocon.commit()
			# print insertwordline
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
