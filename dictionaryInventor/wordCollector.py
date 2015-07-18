# -*- coding: utf-8 -*-
import urllib
import chardet
from pyquery import PyQuery as pq
import string
import re
import urllib2
import lxml.html
import codecs
from selenium import webdriver
from microsofttranslator import Translator
from wordBank import WordBank
import traceback
MAX_URL_COUNTS = 400
# translator = Translator('skeven', 'vizaHdZEjZkP0ZdL/B3CQ0UO9yzsgmTT2hDtuvJFdL0=')
translator = Translator('shosekine', '2GFvzrRkechE3izlMfvRHRs+0y9VEcwpMUvVJhkPVOM=')

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

'''
入力　list(url)...url = 'http;//www.sekine.com/index'
出力　list(word)...word = 'environment'
入力にあるページにあるpタグの言語を抽出して１単語ずつのリストにして返す
'''
def extractwords_fromwebpagelist(urls):
    driver = webdriver.PhantomJS()
    returnwords = []
    # 各サイトの文字コードを判別
    detected = []
    for url in urls:
        print 'PARSE START'
        driver.get(url)
        root = lxml.html.fromstring(driver.page_source)
        links = root.cssselect('p')
        for link in links:  # pタグで抜出し
            if not isinstance(link.text, unicode):
                try:
                    guess = chardet.detect(link.text)
                    link.text = link.text.decode(guess['encoding'])
                except Exception, e:
                    # print 'encoding error'
                    pass
            try:
                #スペースで区切る（単語区切り）
                words = link.text.split();
                for word in words:
                    # print word
                    word = re.sub(r'[!,\",#,$,%,&,\',\(,\),“,”,‘,’,\*,+,\-,\,,.,/,:,;,<,=,>,?,@,\^,_,{,|,},~]+', "", word)
                    word = re.sub(r'[0-9,_]+', "", word)
                    word = string.replace(word, u'“', u'')
                    word = string.replace(word, u'”', u'')
                    word = string.replace(word, u'`', u'')
                    word = string.replace(word, u'‘', u'')
                    word = word.lower()#小文字に変換
                    #ヨーロッパアクセント文字の変換
                    word = strip_accents(word)
                    if word != '\r\n' and word != '' and len(word) >= 2:#1文字のものは削除
                        try:
                            if not isinstance(word, unicode):
                                raise 'not unicode error'
                            wordline = (u'pol', word, u'ja')
                            done = dbinstance.registWord(wordline)
                            print done
                            WordBank.con.commit()
                            returnwords.append(word)
                        except Exception, e:
                            print traceback.format_exc()
                            pass
            except Exception, e:
                print traceback.format_exc()
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
                                    # print len(newurls)
                                    if len(newurls) > MAX_URL_COUNTS:
                                        raise Exception ('Interaption')
                            except Exception, e:
                                if len(newurls) > MAX_URL_COUNTS:
                                    # print 'exception1'
                                    raise Exception ('Interaption')
                                else:
                                    # print 'exception1_sub'
                                    print len(newurls)
                                    pass
        except Exception, e:
            if len(newurls) > MAX_URL_COUNTS:
                # print 'exception2'
                break
            else:
                # print 'exception2_sub'
                # print len(newurls)
                pass
 
    #集めた新しいurlリンク集まりで単語パースするurlのリストを作る
    wordextraction_targeturls = []
    for url in newurls:
        wordextraction_targeturls.append(url['base'])
    return wordextraction_targeturls

def translateword(word, to_language):
    # from_languageは自動的に判別されるので指定する必要が無い
    translated_word = translator.translate(word, to_language)
    detect_language = translator.detect_language(word)
    return {"valueword" : translated_word, "languagetype" : detect_language}

if __name__ == '__main__':
    urls = [
    {'base' : 'http://www.lemonde.fr/'                ,'absolute' : 'http://www.lemonde.fr'},
    {'base' : 'http://www.la-croix.com/'              ,'absolute' : 'http://www.la-croix.com'},
    {'base' : 'http://www.liberation.fr/'             ,'absolute' : 'http://www.liberation.fr'},
        ]
    targeturls = []
    targeturls = getlinkurllist(urls)
    print 'EXTRACTING BEGIN'
    # targeturls = [
    # 'http://www1.folha.uol.com.br/poder/2015/06/1650009-em-derrota-do-governo-senado-aprova-reajuste-para-servidores-do-judiciario.shtml',
    # ]
    dbinstance = WordBank()
    words = []
    words = extractwords_fromwebpagelist(targeturls)
    # for word in words:
    #     wordline = (u'pol', word, u'ja')
    #     done = dbinstance.registWord(wordline)
        # print done
    WordBank.con.close()
        # print word
        # word_atom = translateword(word, 'ja')
        # print u'結果 %s' % word_atom




