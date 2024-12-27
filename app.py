from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database initialization
def init_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            joining_date TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    conn = get_db()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        joining_date = request.form['joining_date']
        
        conn = get_db()
        conn.execute('INSERT INTO employees (name, email, department, joining_date) VALUES (?, ?, ?, ?)',
                    (name, email, department, joining_date))
        conn.commit()
        conn.close()
        
        flash('Employee added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        joining_date = request.form['joining_date']
        
        conn.execute('UPDATE employees SET name=?, email=?, department=?, joining_date=? WHERE id=?',
                    (name, email, department, joining_date, id))
        conn.commit()
        flash('Employee updated successfully!')
        return redirect(url_for('index'))
    
    employee = conn.execute('SELECT * FROM employees WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = get_db()
    conn.execute('DELETE FROM employees WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('Employee deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
