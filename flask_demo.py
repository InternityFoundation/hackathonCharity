from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')



@app.route('/new_register', methods=['GET', 'POST'])
def new_register():
	if request.method == 'POST':
		return redirect('/success')

	return render_template('new_register.html')

@app.route('/success',methods=['GET','POST'])
def success():
    if request.method == 'POST':
        return redirect('/index_login')
    return render_template('success.html')

'''@app.route('/forgot_pwd',methods=['GET','POST'])
def forgot_pwd():
    if request.method == 'POST':
        return redirect('/New_pwd')
    return render_template('forgot_pwd.html')

@app.route('/success',methods=['GET','POST'])
def success():
    if request.method == 'POST':
        return redirect('/index_login')
    return render_template('New_pwd.html')'''


@app.route('/index_login', methods=['GET', 'POST'])
def index_login():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO endUser(name, email, password) VALUES(%s, %s , %s)",(name, email,password))
        mysql.connection.commit()
        cur.close()
        return redirect('/end_user')
    return render_template('index_login.html')

@app.route('/end_user')
def end_user():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM endUser")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('end_user.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)