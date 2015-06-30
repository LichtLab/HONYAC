# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq

# テスト用URL
# METAタグでcharset指定してなくてもちゃんと文字コード判別できるかもテスト
urls = [
    'http://www.yahoo.co.jp/',               # UTF-8
    'https://br.yahoo.com/',              # EUC-JP
    ]


if __name__ == '__main__':
    # 各サイトの文字コードを判別
    detected = []
    for url in urls:
        data = ''.join(urllib.urlopen(url).readlines())
        guess = chardet.detect(data)
        result = dict(url=url,data=data,**guess)
        detected.append(result)

    # 各サイトごとにpタグの文字とリンク先を引っ張ってくる
    for p in detected:
        print '%s -> %s (%s)' % (p['url'], p['encoding'], p['confidence'])
        unicoded = p['data'].decode(p['encoding'])  # デコード
        d = pq(unicoded)
        for link in d.find('p'):  # 見つけたaタグごとにタイトルとURLを抜き出す
            link_title = pq(link).text()
            if link_title != '\r\n':
	            try:
	            	print link_title
	            except:
	            	print 'err'