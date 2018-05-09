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
		# password = hashlib.md5(password.encode()).hexdigest()
		cursor.execute("SELECT * FROM `user` WHERE `uname`='%s' AND `pass`='%s'" % (uname, password))
		data = cursor.fetchone()
		if data:
			return json.dumps({"uid":data[0], "email":data[3]})
		else:
			return json.dumps({"status":0})
	elif request.method == 'GET':
		abort(405)

@app.route('/api/register', methods=['POST'])
def api_register():
	password = hashlib.md5(password.encode()).hexdigest()
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		cursor.execute("INSERT INTO `user` (`uname`, `pass`, `email`) VALUES ('%s', '%s', '%s')" % (uname, password, email))
		conn.commit()
		return json.dumps({"status":1})
	except Exception as e:
		if "Duplicate" in str(e):
			return json.dumps({"status":2})
		else:
			return json.dumps({"status":0})

@app.route('/api/insert/<uid>', methods=['GET'])
def api_insert(uid):
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		folder = request.args['folder']
		title = request.args['title']
		last_position = request.args['last_position']
		duration = request.args['duration']
		temp = title
		file_id = hashlib.md5(temp.encode()).hexdigest()
		cursor.execute("INSERT INTO `list` VALUES ('%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE folder='%s', title='%s', last_position='%s', duration='%s'" 
			% (file_id, uid, folder, title, last_position, duration, folder, title, last_position, duration))
		conn.commit()
		return json.dumps({"status":1})
	except Exception as e:
		return json.dumps({"status":0})

if __name__ == "__main__":
	app.run()