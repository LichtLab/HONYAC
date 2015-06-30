# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq
import string
import re

# 抜き出すURL
urls = [
    'https://esportes.yahoo.com/noticias/guerrero-peru-luta-mas-chile-vence-decide-copa-012402749--spt.html',               # UTF-8
    'https://br.yahoo.com/',              # EUC-JP
    ]


def extractwords():
	 # 各サイトの文字コードを判別
    detected = []
    for url in urls:
        data = ''.join(urllib.urlopen(url).readlines())
        guess = chardet.detect(data)
        result = dict(url=url,data=data,**guess)
        detected.append(result)

    # 各サイトごとに特定タグの文字とリンク先を引っ張ってくる
    for p in detected:
        print '%s -> %s (%s)' % (p['url'], p['encoding'], p['confidence'])
        unicoded = p['data'].decode(p['encoding'])  # デコード
        d = pq(unicoded)
        for link in d.find('p'):  # pタグで抜出し
            link_title = pq(link).text()
            #スペースで区切る（単語区切り）
            words = link_title.split();
            for word in words:
            	word.rstrip('\W')
            	#英数字以外を削除
            	word = re.sub(r'[\W]+', "", word)#英数字以外の文字を削除
            	word = re.sub(r'[0-9,_]+', "", word)#数字、アンダースコアを削除
            	word = word.lower()#小文字に変換
            	if word != '\r\n' and word != '' and len(word) >= 2:#1文字のものは削除
            		try:
            			print word
            		except:
            			pass

if __name__ == '__main__':
   extractwords()