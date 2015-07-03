# -*- coding: utf-8 -*-
import sqlite3
import chardet
import traceback
 
class WordBank:
    # sqliteは同時接続できないのでdbコネクションはクラス変数
    con = sqlite3.connect("wordBank.db")
    cur = con.cursor()
     
    def __init__(self):
        # テーブルがまだ存在してなければ作る
        try:
            WordBank.cur.execute("""CREATE TABLE wordTable(from_language text, from_word text, count integer, to_language text, to_word text);""")
        except Exception, e:
            print 'Target Table already exist'
            pass
 
    def isNewWord(self, word):
        word = (word,)
        WordBank.cur.execute("SELECT from_word FROM wordTable WHERE from_word=?", word)
        if WordBank.cur.fetchone():
            return False
        else:
            return True
 
    def getwordCount(self, word):
        word = (word,)
        WordBank.cur.execute("SELECT from_word, count FROM wordTable WHERE from_word=?", word)
        count = WordBank.cur.fetchone()[1]
        return count
     
    # wordline = ('from_language', 'from_word', 'to_language')
    def registWord(self, wordline):
        # 登録する単語が既に無いかのチェック
        try:
            targetword = wordline[1]
            isNew = self.isNewWord(targetword)
            # print 'isNewword:%s' % COUNT
            if isNew == True:
                # 新しい単語をDBに保存
                targetword_count = 1
                # 本来はここで翻訳
                tranlated_word = ''
                insertwordline = (wordline[0], wordline[1], targetword_count, tranlated_word, wordline[2]) 
                print insertwordline
                WordBank.cur.execute("INSERT INTO wordTable(from_language, from_word, count, to_language, to_word) VALUES (?, ?, ?, ?, ?)", insertwordline)
                print 'INSERTING DONE'
                return True
            else:
                # 既にある単語は登場回数をインクリメント
                count = self.getwordCount(targetword)
                count = count + 1
                # targetwordに対してupdate
                WordBank.cur.execute("UPDATE wordTable set count=? WHERE from_word=?", (count, targetword))
                print 'UPDATING DONE'
                return True
        except Exception, e:
            print traceback.format_exc()
            return False
 
    def printrecodelist(self):
        print 'RECORD LIST:::'
        WordBank.cur.execute("SELECT from_word, count FROM wordTable;")
        for d in WordBank.cur.fetchall():
            print 'word:%s, count:%s' % (d[0], str(d[1]))
 
 
dbinstance = WordBank()
wordline = (u'pol', u'amigo', u'ja')
done = dbinstance.registWord(wordline)
dbinstance.printrecodelist()
WordBank.con.commit()
WordBank.con.close()