# encoding: utf-8
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
@app.route("/")
def index():
	return 'CONNECTION OK'

if __name__ == '__main__':
	context = ('./securekey/honyak.crt', './securekey/honyak.key')
	app.run(host='0.0.0.0', port=8000, ssl_context=context, threaded=True, debug=True)