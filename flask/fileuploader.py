# encoding: utf-8
import os
import json
import datetime
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

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

@app.route('/translateword', methods=['POST'])
def translate():
	missingword = request.form['missingword']
	from_language = request.form['from_language']
	to_language = request.form['to_language']
	# Translate this word from [from_language] to [to_language] by ms translator
	# Registering Word to DB(CSV?)

	#server side must have internet connection(if dont, no client)
	translated_word = ""
	return translated_word;

@app.route('/searchquerylog', methods=["POST"])
def registlogs():
	userid = request.form['userid']
	searchword = request.form['searchword']
	timestamp = request.form['timestamp']
	# missing event & word typing event
	#その単語を検索しているユーザはどんなバックグラウンドを持ったユーザなのかを登録したいが。。。

	#googleのスペルチェックAPIが使えるっぽい


if __name__ == '__main__':
    app.run()