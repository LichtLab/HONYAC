# -*- coding: utf-8 -*-
import sqlite3
import chardet
import traceback
import re
import string
from langdetect import detect

def WordBankCleaner():
    # sqliteは同時接続できないのでdbコネクションはクラス変数
    con = sqlite3.connect("wordBank.db")
    cur = con.cursor()
    cur.execute("SELECT to_word FROM wordTable;")
    iteration = 0
    for d in cur.fetchall():
        if d[0].find('[a-z]'):
            query = "DELETE FROM wordTable where to_word = '%s' " % d[0]
            cur.execute(query)
            con.commit()
            print 'DONE%s' % iteration
            iteration = iteration + 1

if __name__ == '__main__':
    # con = sqlite3.connect("wordBank.db")
    # cur = con.cursor()
    # cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")
    # WordBankCleaner()
    # string = detect(u"生年月日")
    # print string
    string = u'これは9です'
    if re.search("[a-z]",string):
        print 'OK'
    else:
        print 'NG'