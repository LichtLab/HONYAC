# -*- coding: utf-8 -*-
import sqlite3
import chardet
import traceback
from microsofttranslator import Translator
translator = Translator('skeven', 'vizaHdZEjZkP0ZdL/B3CQ0UO9yzsgmTT2hDtuvJFdL0=')

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
                # ここで翻訳
                tmp = self.translateword(targetword, u'ja')
                detect_language = tmp[0]
                translated_word = tmp[1]
                insertwordline = (detect_language, targetword, targetword_count, translated_word, wordline[2]) 
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
        WordBank.cur.execute("SELECT from_language, from_word, count, to_language, to_word FROM wordTable;")
        for d in WordBank.cur.fetchall():
            print '(%s, %s, %s, %s, %s)' % (d[0], str(d[1]), d[2], d[3], d[4])
    def translateword(self, word, to_language):
        # from_languageは自動的に判別されるので指定する必要が無い
        translated_word = translator.translate(word, to_language)
        detect_language = translator.detect_language(word)
        return (detect_language, translated_word)
        # return {"valueword" : translated_word, "languagetype" : detect_language}

 
# dbinstance = WordBank()
# wordline = (u'pol', u'gracie', u'ja')
# done = dbinstance.registWord(wordline)
# dbinstance.printrecodelist()
# WordBank.con.commit()
# WordBank.con.close()

