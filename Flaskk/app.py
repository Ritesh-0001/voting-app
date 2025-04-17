from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", ""),
    database=os.environ.get("DB_NAME", "voting_app")
)
cursor = db.cursor(dictionary=True)
print(cursor)

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/vote')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, passwd))
        user = cursor.fetchone()
        if user:
            session['username'] = uname
            session['user_id'] = user['id']
            return redirect('/vote')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, passwd))
            db.commit()
            return redirect('/login')
        except mysql.connector.errors.IntegrityError:
            return render_template('signup.html', error='Username already exists!')
    return render_template('signup.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        team = request.form['team']
        user_id = session['user_id']
        cursor.execute("INSERT INTO votes (user_id, team) VALUES (%s, %s)", (user_id, team))
        db.commit()
        return redirect('/results')
    return render_template('vote.html')

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect('/login')

    cursor.execute("SELECT team, COUNT(*) as count FROM votes GROUP BY team")
    vote_data = cursor.fetchall()
    vote_result = {row['team']: row['count'] for row in vote_data}
    return render_template('result.html', votes=vote_result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
