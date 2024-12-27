from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages
EXCEL_FILE = 'employees.xlsx'

# Create Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['id', 'name', 'email', 'department', 'joining_date', 'status'])
    df.to_excel(EXCEL_FILE, index=False)

def load_employees():
    return pd.read_excel(EXCEL_FILE)

def save_employees(df):
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    df = load_employees()
    return render_template('index.html', employees=df.to_dict('records'))

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        df = load_employees()
        new_id = len(df) + 1
        
        new_employee = {
            'id': new_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'department': request.form['department'],
            'joining_date': request.form['joining_date'],
            'status': 'Active'
        }
        
        df = df.append(new_employee, ignore_index=True)
        save_employees(df)
        flash('Employee added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    df = load_employees()
    if request.method == 'POST':
        df.loc[df['id'] == id, 'name'] = request.form['name']
        df.loc[df['id'] == id, 'email'] = request.form['email']
        df.loc[df['id'] == id, 'department'] = request.form['department']
        df.loc[df['id'] == id, 'joining_date'] = request.form['joining_date']
        save_employees(df)
        flash('Employee updated successfully!')
        return redirect(url_for('index'))
    
    employee = df[df['id'] == id].to_dict('records')[0]
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    df = load_employees()
    df = df[df['id'] != id]
    save_employees(df)
    flash('Employee deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
