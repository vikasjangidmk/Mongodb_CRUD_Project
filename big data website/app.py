from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['employee']


import re

def validate_employee_data(emp_id, name, email, desig, city):
    # Check if roll_no already exists
    if db.employee.find_one({'emp_id': emp_id}):
        return False, 'Employee id already exists'
    # Email validation
    if not re.match(r"^((\w+)|(.|_))+@(\w+).(\w+)$", email):
        return False, 'Invalid email address'
    # Add more validations for other fields if required
    return True, None



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_id = request.form['emp_id']
        name = request.form['name']
        email = request.form['email']
        desig = request.form['designation']
        city = request.form['city']

        is_valid, error_message = validate_employee_data(employee_id, name, email, desig, city)
        if is_valid:
            db.employee.insert_one({'emp_id': employee_id, 'name': name, 'email': email, 'designation': desig, 'city': city})
            return redirect(url_for('home'))
        else:
            return error_message

    return render_template('add_employee.html')


@app.route('/show_employee', methods=['GET', 'POST'])
def show_employee():
    error_message = None
    employee = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        employee = db.employee.find_one({'emp_id': emp_id})
        if not employee:
            error_message = 'Employee with employee {} does not exist'.format(emp_id)
    return render_template('show_employee.html', employee=employee, error_message=error_message)



@app.route('/update_employee', methods=['GET', 'POST'])
def update_employee():
    error_message = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        existing_employee = db.employee.find_one({'emp_id': emp_id})
        if not existing_employee:
            error_message = 'Employee with ID {} does not exist'.format(emp_id)
        else:
            new_name = request.form['name']
            new_email = request.form['email']
            new_desig = request.form['designation']
            new_city = request.form['city']

            
            db.employee.update_one({'emp_id': emp_id}, {'$set': {'name': new_name, 'email': new_email, 'designation': new_desig, 'city': new_city}})
            return redirect(url_for('home'))


    return render_template('update_employee.html', error_message=error_message)




@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    error_message = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        existing_employee = db.employee.find_one({'emp_id': emp_id})
        if not existing_employee:
            error_message = 'Employee with ID {} does not exist'.format(emp_id)
        else:
            db.employee.delete_one({'emp_id': emp_id})
            return redirect(url_for('home'))
    return render_template('delete_employee.html',error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
