from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bharathsql@123'
app.config['MYSQL_DB'] = 'login_page'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect('/dashboard')
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return redirect('/dashboard')


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

    return redirect('/dashboard')


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

    
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        mysql.connection.commit()
        cur.close()

        return redirect('/dashboard')

    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('edit_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)


