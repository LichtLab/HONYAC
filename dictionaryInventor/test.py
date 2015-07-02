# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq
import string
import re
import urllib2
import lxml.html
import codecs
MAX_URL_COUNTS = 500
 
 
'''
入力　list(url)...url = 'http;//www.sekine.com/index'
出力　list(word)...word = 'environment'
入力にあるページにあるpタグの言語を抽出して１単語ずつのリストにして返す
'''
def extractwords_fromwebpagelist(urls):
    returnwords = []
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
            #ここでstrになる可能性があるのでunicodeに変換する
            link_title = pq(link).text()
            if not isinstance(link_title, unicode):
                guess = chardet.detect(link_title)
                link_title = link_title.decode(guess['encoding'])
            #スペースで区切る（単語区切り）
            words = link_title.split();
            for word in words:
                # word = re.sub(re.compile("[!-/:-@[-`{-~]"), '', word)
                word = re.sub(r'[!,\",#,$,%,&,\',\(,\),*,+,-,\,,.,/,:,;,<,=,>,?,@,\^,_,{,|,},~]+', "", word)
                word = re.sub(r'[0-9,_]+', "", word)
                word = word.lower()#小文字に変換
                if word != '\r\n' and word != '' and len(word) >= 2:#1文字のものは削除
                    try:
                        if not isinstance(word, unicode):
                            print 'not unicode error'
                            raise 'not unicode error'
                        returnwords.append(word)
                    except Exception, e:
                        print 'exeption0'
                        pass
    return returnwords
 
'''
入力　list(dic)...dic = {'base' : 'http;//www.sekine.com/index', 'absolute' : 'http;//www.sekine.com'}
出力　list(url)...url = 'http;//www.sekine.com/index'
入力にあるページにあるリンクを抽出してurl文字列のリストとして返す。相対パスは絶対パスに変換される
'''
def getlinkurllist(url_diclist):
    newurls = urls
    #登録したスタート地点のリンクでループ
    for targeturl in urls:
        try:
            html = urllib2.urlopen(targeturl['base']).read()
            dom = lxml.html.fromstring(html)
            dom.make_links_absolute(targeturl['absolute'])
            links_from_targeturl = dom.xpath("//@href")
            print 'begin url parsing'
            print targeturl['base']
            #リンク先の全てのurlをチェック
            for urlele in links_from_targeturl:
                if urlele.find('http') or urlele.find('https'):
                    #特定のリンク先を落とすフィルタリング
                    if not urlele.find('css') or not urlele.find('jpg') or not urlele.find('png') or not urlele.find('js') or urlele.find('javascript'): 
                        if urlele.find('mail'):
                            try:
                                #urleleが既に登録済みのリンクでないかをチェック
                                existingflag = False
                                for targeturl_sub in newurls:
                                    if targeturl_sub['base'] == urlele:
                                        existingflag = True
                                if existingflag == False:
                                    #print urlele
                                    newurl_dic = {'base': urlele, 'absolute': targeturl['absolute']}
                                    newurls.append(newurl_dic)
                                    print len(newurls)
                                    if len(newurls) > MAX_URL_COUNTS:
                                        raise Exception ('Interaption')
                            except Exception, e:
                                if len(newurls) > MAX_URL_COUNTS:
                                    print 'exception1'
                                    raise Exception ('Interaption')
                                else:
                                    print 'exception1_sub'
                                    print len(newurls)
                                    pass
        except Exception, e:
            if len(newurls) > MAX_URL_COUNTS:
                print 'exception2'
                break
            else:
                print 'exception2_sub'
                print len(newurls)
                pass
 
    #集めた新しいurlリンク集まりで単語パースするurlのリストを作る
    wordextraction_targeturls = []
    for url in newurls:
        wordextraction_targeturls.append(url['base'])
    return wordextraction_targeturls
 
 
if __name__ == '__main__':
    urls = [
    {'base' : 'http://www.correiobraziliense.com.br/'   ,'absolute' : 'http://www.correiobraziliense.com.br'},
    {'base' : 'http://www.em.com.br/'                   ,'absolute' : 'http://www.em.com.br'},
    {'base' : 'http://www.estadao.com.br/'              ,'absolute' : 'http://www.estadao.com.br'},
    {'base' : 'http://www.folha.com/'                   ,'absolute' : 'http://www.folha.com'},
    {'base' : 'http://oglobo.globo.com/'                ,'absolute' : 'http://oglobo.globo.com'},
    {'base' : 'http://www.zerohora.com'                 ,'absolute' : 'http://www.zerohora.com'},
        ]
    # targeturls = []
    # targeturls = getlinkurllist(urls)
    print 'EXTRACTING BEGIN'
    testurl = [
    'http://www1.folha.uol.com.br/poder/2015/06/1650009-em-derrota-do-governo-senado-aprova-reajuste-para-servidores-do-judiciario.shtml',
    ]
    words = []
    words = extractwords_fromwebpagelist(testurl)
    # for word in words:
        # print type(word)
        # print word
    f = codecs.open('text.txt', 'w', 'utf-8')
    for word in words:
        if not isinstance(word, unicode):
            print 'not unicode error'
            # raise 'not unicode error'
        word = word + '\n'
        f.write(word)
    f.close()