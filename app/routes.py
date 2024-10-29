
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
import os


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")
  
  
@main.route('/role_selection')
def role_selection():
  return render_template('role.html')

@main.route('/handle_role', methods=['POST'])
def handle_role():
    role = request.form.get('role')
    if role == 'customer':
        return redirect(url_for('main.register_customer'))
    elif role == 'owner':
        return redirect(url_for('main.register_owner'))
    return redirect('/role_selection')




@main.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
    
            name = request.form.get('name')
            email = request.form.get('email')
            password = generate_password_hash(request.form.get('password'))
            address = request.form.get('address')
            special_needs = request.form.get('special_needs')
            gender = request.form.get('gender')
            
            existing_user = mongo.db.customers.find_one({'email': email})
            if existing_user:
                flash('Email already exists')
                return redirect(url_for('main.register_customer'))
            
            mongo.db.customers.insert_one({
                'name': name,
                'email': email,
                'password': password,
                'address': address,
                'special_needs': special_needs,
                'gender': gender})
            
            
            return redirect(url_for('main.index'))
            
    
    
    return render_template('register_customer.html')


@main.route('/register_owner', methods=['GET', 'POST'])
def register_owner():
    if request.method == 'POST':
            restaurant_name = request.form.get('restaurant_name')
            restaurant_address = request.form.get('restaurant_address')
            owner_name = request.form.get('owner_name')
            email = request.form.get('email')
            username = request.form.get('username')
            password = generate_password_hash(request.form.get('password'))
            opening_hours = {}
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            existing_user = mongo.db.owners.find_one({'email': email})
            if existing_user:
                flash('Email already exists')
                return redirect(url_for('main.register_owner'))
            

            for day in days:
                open_time = request.form.get(f'{day.lower()}_open')
                close_time = request.form.get(f'{day.lower()}_close')
                if open_time and close_time:
                    opening_hours[day] = {'open': open_time, 'close': close_time}
                else:
                    opening_hours[day] = None
                    
                    
                    
                    
            mongo.db.owners.insert_one({
                 'restaurant_name': restaurant_name,
                 'restaurant_address': restaurant_address,
                 'opening_hours': opening_hours,
                 'owner_name': owner_name,
                 'email': email,
                 'username': username,
                 'password': password
                 })
            
           
            return redirect(url_for('main.index'))
                
    return render_template('register_owner.html')


@main.route('/customer_dashboard')
def customer_dashboard():
     return render_template('customer_dashboard.html')


@main.route('/owner_dashboard')
def owner_dashboard():
     return render_template('owner_dashboard.html')

@main.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        if request.form["username"] == "123" and request.form["pswd"] == "123":
            return render_template("index.html")
        else:
            return render_template("login.html", failed=True)
    else:
        return render_template("login.html")

