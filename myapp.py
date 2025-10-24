from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask (__name__)
app.secret_key = '!@#$%'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MySQL_DB'] = 'flaskmysql'

mysql = MySQL(app)

# set route default dan http method yang diizinkan
@app.route('/', methods=['GET', 'POST'])
def login():
    # cek jika method POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        # ambil data dari form
        email = request.form['inpEmail']
        passwd = request.form['inpPass']

        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, passwd))

        # fetch hasil kueri
        result = cur.fetchone()

        # cek hasil kueri
        if result:
            # jika login valid buat data session
            session['is_logged_in'] = True
            session['username'] = result[1]   # ambil kolom username
            # Redirect ke halaman home
            return redirect(url_for('home'))
        else:
            # jika login invalid kembalikan ke login form
            return render_template('login.html')
    else:
        # jika method selain POST tampilkan form login
        return render_template('login.html')


# route untuk halaman home
@app.route('/home')
def home():
    # hanya bisa diakses jika sudah login
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        return render_template('home.html', users=data)
    else:
        return redirect(url_for('login'))

# route logout
@app.route('/logout')
def logout():
    # hapus data session
    session.pop('is_logged_in', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# debug dan auto reload
if __name__ == '__main__':
    app.run(debug=True)