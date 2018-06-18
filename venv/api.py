from flask import Flask, request, json
from flaskext.mysql import MySQL

import hashlib


app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b8da8322190e16'
app.config['MYSQL_DATABASE_PASSWORD'] = 'c37ae115'
app.config['MYSQL_DATABASE_DB'] = 'heroku_f27f25d37df7958'
app.config['MYSQL_DATABASE_HOST'] = 'mysql://b8da8322190e16:c37ae115@us-cdbr-iron-east-04.cleardb.net/heroku_f27f25d37df7958?reconnect=true'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/number", methods=['POST'])
def post_phonenumber():
    req = request.get_json()
    number = req['number'] 
    obj = hashlib.sha256(number.encode())
    val = obj.hexdigest()
    cursor.execute("SELECT * FROM users WHERE number=\'" + val + "\'")
    row = cursor.fetchone()
    conn.commit()
    if row is None:
        return json.dumps({"msg": "Please enter your name."})
    else:
        stamps = row[2] + 1
        name = row[0]
        if stamps == 11:
            cursor.execute("UPDATE users SET stamps=\'0\' WHERE number=\'" + val + "\'")
            return json.dumps({"msg": "Welcome back! Please show this message to claim your free meal!"})
        else:
            cursor.execute("UPDATE users SET stamps=\'" + str(stamps) + "\' WHERE number=\'" + val + "\'")
            return json.dumps({"name": name, "stamps": stamps})

@app.route("/signup", methods=['POST'])
def signup():
    req = request.get_json()
    number = req['number']
    name = req['name']
    obj = hashlib.sha256(number.encode())
    val = obj.hexdigest()
    cursor.execute("INSERT INTO users (name, number, stamps) VALUES (\'" + name + "\', \'" + val +  "', '1')")
    conn.commit()
    return json.dumps({"name": name, "stamps": 1})

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5001)