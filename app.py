from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for login session

# Admin login credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    place = request.form['place']
    description = request.form['description']

    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("INSERT INTO complaints (name, email, date, place, description) VALUES (?, ?, ?, ?, ?)",
              (name, email, date, place, description))
    conn.commit()
    conn.close()

    return 'Complaint submitted successfully!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/view')
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/view')
def view_complaints():
    if not session.get('admin'):
        return redirect('/login')
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    data = c.fetchall()
    conn.close()
    return render_template('view.html', complaints=data)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)