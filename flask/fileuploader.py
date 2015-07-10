# encoding: utf-8
import os
import json
import datetime
import csv
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from microsofttranslator import Translator

UPLOAD_FOLDER_IMG = './img/'
UPLOAD_FOLDER_TXT = './word/'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'png', 'jpg', 'jpeg'])
app = Flask(__name__)

@app.route("/")
def index():
	return 'CONNECTION OK'

def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadfile', methods=['POST'])
def upload():
	f = request.files["file"]
	print "test1"
	if f and allowed_file(f.filename):
		print "test2"
		filename = secure_filename(f.filename)
		fileextention = filename.rsplit('.', 1)[1]
		if fileextention == 'png' or fileextention == 'jpg' or fileextention == 'jpeg' :
			UPLOAD_FOLDER = UPLOAD_FOLDER_IMG
		else:
			UPLOAD_FOLDER = UPLOAD_FOLDER_TXT
		print "test3"
		now = datetime.datetime.now()
		fileetitle = filename.rsplit('.', 1)[0]
		filename_save = fileetitle + "{0:%Y-%m-%d-%H-%M-%S}".format(now) + "." + fileextention
		f.save(os.path.join(UPLOAD_FOLDER, filename_save))
		return "OK"
	return "ERR"

@app.route('/translateword', methods=['GET','POST'])
def translate():
	#missingword = request.form['missingword']
	#to_language = request.form['to_language']
	missingword = 'envelope'
	to_language = 'ja'
	#from_language = request.form['from_language']

	#翻訳
	print '1step'
	translator = Translator('skeven', 'vizaHdZEjZkP0ZdL/B3CQ0UO9yzsgmTT2hDtuvJFdL0=')
	# from_languageは自動的に判別されるので指定する必要が無い
	translated_word = translator.translate(missingword, to_language)
	print '2step'
	#translated_word = translator.translate("Hello", "ja")
	# Registering Word to DB(CSV?)
	languagetype = translator.detect_language(missingword)
	print '3step'

	inlinecsv = languagetype + '$YIN$' + missingword + '$YIN$' + to_language + "$YIN$" + translated_word + '\n'
	print inlinecsv
	f = open('./word/addinfo_dictionary_utf8.txt', 'a')
	f.write(inlinecsv.encode('utf-8'))
	f.close()
	return translated_word;

@app.route('/searchquerylog', methods=["POST"])
def registlogs():
	userid = request.form['userid']
	searchword = request.form['searchword']
	timestamp = request.form['timestamp']
	# missing event & word typing event

	inlineyinsv = userid + '$YIN$' + timestamp + '$YIN$' + searchword + '\n'
	f = open('./searchlog/searchlog.txt', 'a')
	f.write(inlinecsv.encode('utf-8'))
	f.close()
	#その単語を検索しているユーザはどんなバックグラウンドを持ったユーザなのかを登録したいが。。。
	#googleのスペルチェックAPIが使えるっぽい
	return 'OK'

if __name__ == '__main__':
	context = ('./securekey/honyak.crt', './securekey/honyak.key')
	app.run(host='0.0.0.0', port=8000, ssl_context=context, threaded=True, debug=True)