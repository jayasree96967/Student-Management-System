from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create student table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def home():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
        (name, email, course)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
