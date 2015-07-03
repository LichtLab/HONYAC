import lxml.html
from selenium import webdriver
import codecs
import chardet

target_url = 'http://www1.folha.uol.com.br/poder/2015/06/1650009-em-derrota-do-governo-senado-aprova-reajuste-para-servidores-do-judiciario.shtml'
driver = webdriver.PhantomJS()
driver.get(target_url)
root = lxml.html.fromstring(driver.page_source)
links = root.cssselect('p')
for link in links:
	if not isinstance(link.text, unicode):
		guess = chardet.detect(link.text)
		link.text = link.text.decode(guess['encoding'])
		print 'encoded'
	print link.text