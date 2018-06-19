from flask import Flask, request, json
from flaskext.mysql import MySQL

import hashlib, datetime


app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b8da8322190e16'
app.config['MYSQL_DATABASE_PASSWORD'] = 'c37ae115'
app.config['MYSQL_DATABASE_DB'] = 'heroku_f27f25d37df7958'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-04.cleardb.net'
mysql.init_app(app)

@app.route("/number", methods=['POST'])
def post_phonenumber():
    conn = mysql.connect()
    cursor = conn.cursor()
    req = request.get_json()
    number = req['number'] 
    obj = hashlib.sha256(number.encode())
    val = obj.hexdigest()
    cursor.execute("SELECT * FROM users WHERE number=\'" + val + "\'")
    row = cursor.fetchone()
    now = datetime.datetime.now()
    limit = datetime.timedelta(hours=1)   
    if row is None:
        cursor.close()
        return json.dumps({"msg": "Please enter your name."})
    else:
        timeDifference = now - row[3]
        isPastLimit = timeDifference < limit
        if isPastLimit:
            cursor.close()
            return json.dumps({"msg": "I'm sorry, but you can only check in once a day."})
        stamps = int(row[2]) + 1
        name = row[0]
        if stamps == 11:
            cursor.execute("UPDATE users SET stamps=\'0\' WHERE number=\'" + val + "\'")
            conn.commit()
            cursor.close()
            return json.dumps({"msg": "Welcome back! Please show this message to claim your free meal!"})
        else:
            cursor.execute("UPDATE users SET stamps=\'" + str(stamps) + "\' WHERE number=\'" + val + "\'")
            conn.commit()
            cursor.close()
            return json.dumps({"name": name, "stamps": stamps})

@app.route("/signup", methods=['POST'])
def signup():
    conn = mysql.connect()
    cursor = conn.cursor()
    req = request.get_json()
    number = req['number']
    name = req['name']
    obj = hashlib.sha256(number.encode())
    val = obj.hexdigest()
    cursor.execute("INSERT INTO users (name, number, stamps, date) VALUES (\'" + name + "\', \'" + val +  "', '1', NOW())")
    conn.commit()
    cursor.close()
    return json.dumps({"name": name, "stamps": 1})

if __name__ == "__main__":
        app.run(debug=True)