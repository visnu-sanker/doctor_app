from flask import Flask,render_template, request, jsonify, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'doctor'

app.secret_key = 'your secret key'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM doctorlist''')
    result = cur.fetchall()
    print (result)
    return jsonify(result)


@app.route('/doclist',methods=['GET'])
def doc_list():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute('''SELECT * FROM doctorlist''')
        result = cur.fetchall()
        print (result)
        return jsonify(result)

        

@app.route("/doclist/<int:id>", methods=["GET", "PUT"])
def specific_doctor(id):
    cur = mysql.connection.cursor()
    doctor = None
    if request.method == "GET":
        cur.execute("SELECT * FROM doctorlist WHERE Id=%s", (id,)) 
        rows = cur.fetchall()
        for r in rows:
            doctor = r
        if doctor is not None:
            return jsonify(doctor), 200
        else:
            return "Something went wrong", 404



@app.route('/login', methods=['GET','POST'])
def login_doctor():
    if request.method == "POST":
        log = True
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM doctorlist WHERE email = %s AND password = %s', (email, password,))
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['Id'] = user['Id']
            session['email'] = user['email']
            return jsonify('User Logged in successfully!')
        else:
            return jsonify('Incorrect username/password!')
 
    return "User logged in successfully!"


@app.route("/logout")
def logout_doctor():
    session.clear()
    return jsonify("User logged out!")




if __name__ == "__main__":
    app.run()