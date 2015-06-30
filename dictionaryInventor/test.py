# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq
import string
import re
import urllib2
import lxml.html

URL_ABSOLUTE = "http://www.correiobraziliense.com.br"

def extractwords(urls):
	# 各サイトの文字コードを判別
    returnurls = []
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
    urls = [
    {'base' : 'http://www.correiobraziliense.com.br/'   ,'absolute' : 'http://www.correiobraziliense.com.br'},
    {'base' : 'http://www.em.com.br/'                   ,'absolute' : 'http://www.em.com.br'},
    {'base' : 'http://www.estadao.com.br/'              ,'absolute' : 'http://www.estadao.com.br'},
    {'base' : 'http://www.folha.com/'                   ,'absolute' : 'http://www.folha.com'},
    {'base' : 'http://oglobo.globo.com/'                ,'absolute' : 'http://oglobo.globo.com'},
    {'base' : 'http://www.zerohora.com'                 ,'absolute' : 'http://www.zerohora.com'},
        ]
    for url in urls:
        try:
            html = urllib2.urlopen(url['base']).read()
            dom = lxml.html.fromstring(html)
            dom.make_links_absolute(URL_ABSOLUTE)
            urlList = dom.xpath("//@href")
            for urlele in urlList:
                if urlele.find('http') or urlele.find('https'):
                    if not urlele.find('css') or urlele.find('jpg') or urlele.find('png') or urlele.find('js') or urlele.find('javascript'): 
                        try:
                            urldic = {'base': urlele, 'absolute': url['absolute']}
                            print urldic                
                        except Exception, e:
                            pass
        except Exception, e:
            pass

    #urls = extractwords(urls)
    #urls = extractwords(urlList)
    #print urls