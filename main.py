import json
import hashlib
from flask import Flask, request, session
from flaskext.mysql import MySQL
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movie_trek'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/api/login', methods=['POST'])
def api_login():
	if request.method == 'POST':
		cursor = mysql.connect().cursor()
		uname = request.form['username']
		password = request.form['password']
		password = hashlib.md5(password.encode()).hexdigest()
		cursor.execute("SELECT * FROM `user` WHERE `uname`='%s' AND `pass`='%s'" % (uname, password))
		data = cursor.fetchone()
		if data:
			return json.dumps(data)
		else:
			return json.dumps({"status":0})
	elif request.method == 'GET':
		return "NOT ALLOWED"

@app.route('/api/register', methods=['POST'])
def api_register(uname, password, email):
	password = hashlib.md5(password.encode()).hexdigest()
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		cursor.execute("INSERT INTO `user` (`uname`, `pass`, `email`) VALUES ('%s', '%s', '%s')" % (uname, password, email))
		conn.commit()
		return json.dumps({"status":1})
	except Exception as e:
		return json.dumps({"status":0})

@app.route('/api/insert', methods=['GET'])
def api_insert():
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		folder = request.args.get('folder')
		title = request.args.get('title')
		last_position = request.args.get('last_position')
		duration = request.args.get('duration')
		file_id = folder + len(folder) + title
		print(file_id)
		# cursor.execute("INSERT INTO `list` VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % ())
	except Exception as e:
		raise e

@app.route('/api/update/<uid>', methods=['GET'])
def api_update(uid):
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		folder = request.args.get('folder')
		title = request.args.get('title')
		last_position = request.args.get('last_position')
		duration = request.args.get('duration')
		cursor.execute("SELECT * FROM list WHERE id_user='%s' AND title='%s'" % (uid, title))
		data = cursor.fetchone()
		if data:
			cursor.execute("REPLACE INTO list ()")

		return json.dumps({"status":1})
	except Exception as e:
		return json.dumps({"status":0})

if __name__ == "__main__":
	app.run()