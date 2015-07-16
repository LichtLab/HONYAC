from flask import Flask, request, send_from_directory
app = Flask(__name__,static_url_path='')

@app.route('/dbdownload/<dbname>')
def dbdownload(dbname):
    return send_from_directory('db', path)

if __name__ == '__main__':
	app.run()
	# app.run(debug=True)