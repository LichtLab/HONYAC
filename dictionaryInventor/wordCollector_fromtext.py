# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq
import string
import re
import codecs
from wordBank import WordBank
import traceback

if __name__ == '__main__':
    dbinstance = WordBank()


    f = open('portugues_words.txt')
    line = f.readline()
    while line:
        guess = chardet.detect(line)
        line = line.decode('utf-8')
        #スペースで区切る（単語区切り）
        words = line.split();
        for word in words:
            # print word
            word = re.sub(r'[!,\",#,$,%,&,\',\(,\),“,”,‘,’,\*,+,\-,\,,.,/,:,;,<,=,>,?,@,\^,_,{,|,},~]+', "", word)
            word = re.sub(r'[0-9,_]+', "", word)
            word = string.replace(word, u'“', u'')
            word = string.replace(word, u'”', u'')
            word = string.replace(word, u'`', u'')
            word = string.replace(word, u'‘', u'')
            word = word.lower()#小文字に変換
            if word != '\r\n' and word != '' and len(word) >= 2:#1文字のものは削除
                try:
                    if not isinstance(word, unicode):
                        raise 'not unicode error'
                    wordline = (u'pol', word, u'ja')
                    done = dbinstance.registWord(wordline)
                    print done
                    WordBank.con.commit()
                except Exception, e:
                    print traceback.format_exc()
                    pass
        line = f.readline()
    f.close
    WordBank.con.close()