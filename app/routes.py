
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
import os
from bson import ObjectId



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


@main.route('/owner_dashboard')
def owner_dashboard():
    return render_template('owner_dashboard.html')

@main.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer_dashboard.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        customer = mongo.db.customers.find_one({'email': email})
        owner = mongo.db.owners.find_one({'email': email})

        user = customer if customer else owner
        if user and check_password_hash(user['password'], password):
            session['email'] = user['email']
            session['role'] = 'owner' if owner else 'customer'
            dashboard_route = 'main.owner_dashboard' if owner else 'main.customer_dashboard'
            return redirect(url_for(dashboard_route))
        else:
            flash('invalid email or password')
            return render_template('login.html', failed=True)
        
    return render_template("login.html")

@main.route('/customer_profile')
def customer_profile():
    if 'email' not in session:
        flash('You must be logged in to view this page', category='error')
        return redirect(url_for('main.login'))
    customer = mongo.db.customers.find_one({'email': session['email']})
    if not customer:
        flash('Customer profile not found', category='error')
        return redirect(url_for('main.index'))
    return render_template('customer_profile.html', customer=customer)

@main.route('/owner_profile', methods=['GET', 'POST'])
def owner_profile():
    if 'email' not in session or session.get('role') != 'owner':
        flash('You must be logged in and an owner to view this page', category='error')
        return redirect(url_for('main.login'))
    owner = mongo.db.owners.find_one({'email': session['email']})
    if request.method == 'POST':
        updated_data = {
            'owner_name': request.form.get('owner_name'),
            'restaurant_name': request.form.get('restaurant_name'),
            'restaurant_address': request.form.get('restaurant_address'),
            'opening_hours': {
                day: {
                    'open': request.form.get(f'{day.lower()}_open'),
                    'close': request.form.get(f'{day.lower()}_close')
                } for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            }

        }

        mongo.db.owners.update_one({'email': session['email']}, {'$set': updated_data})
        flash('Profile updated successfully', category='success')

        return redirect(url_for('main.owner_profile'))
    
    if owner:
        owner['_id'] = str(owner['_id'])
    return render_template('owner_profile.html', owner=owner)


@main.route('/edit_owner_profile', methods=['GET', 'POST'])
def edit_owner_profile():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    owner = mongo.db.owners.find_one({'email': session['email']})
    if request.method == 'POST':
        updated_data = {
             'owner_name': request.form.get('owner_name'),
            'restaurant_name': request.form.get('restaurant_name'),
            'restaurant_address': request.form.get('restaurant_address'),
            
        }

        mongo.db.owners.update_one({'email': session['email']}, {'$set': updated_data})
        flash('Profile updated successfully', category='success')
        return redirect(url_for('main.owner_profile'))
    return render_template('edit_owner_profile.html', owner=owner)


@main.route('/edit_customer_profile', methods=['POST'])
def edit_customer_profile():
    if 'email' not in session:
        flash('You must be logged in to view this page', category='error')
        return redirect(url_for('main.login'))
    
    email = session['email']
    updated_data = {
        'name': request.form.get('name'),
        'address': request.form.get('address'),
        'special_needs': request.form.get('special_needs'),
        'gender': request.form.get('gender'),
    }
    mongo.db.customers.update_one({'email': email}, {'$set': updated_data})
    flash('Profile updated successfully', category='success')
    return redirect(url_for('main.customer_profile'))



@main.route('/manage_meals')
def manage_meals():
    if 'email' not in session or session.get('role') != 'owner':
        flash("You must be logged in as an owner to view this page.", category='error')
        return redirect(url_for('main.login'))
    

    owner_email = session['email']
    meals = mongo.db.meals.find({'owner_email': owner_email})
    meal_list = [{
        '_id': str(meal['_id']),  
        'name': meal['name'],
        'price': meal['price'],
        'photo': meal['photo'],
        'ingredients': meal['ingredients']
    } for meal in meals]

    return render_template('manage_meals.html', dishes=meal_list)


@main.route('/add_meal', methods=['GET', 'POST'])
def add_meal():
    if 'email' not in session or session.get('role') != 'owner':
        flash("You must be logged in as an owner to view this page.", category='error')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        photo = request.form.get('photo')
        ingredients = [ingredient.strip() for ingredient in request.form.get('ingredients').split(',')]
        mongo.db.meals.insert_one({
            'name': name,
            'price': price,
            'photo': photo,
            'ingredients': ingredients,
            'owner_email': session['email']
        })

        flash("Meal added successfully!", category="success")
        return redirect(url_for('main.manage_meals'))

    return redirect(url_for('main.manage_meals'))
    
    
@main.route('/delete_meal/<meal_id>', methods=['POST'])
def delete_meal(meal_id):
     if 'email' not in session or session.get('role') != 'owner':
        flash("You must be logged in as an owner to delete a meal.", category='error')
        return redirect(url_for('main.login'))
     mongo.db.meals.delete_one({'_id': ObjectId(meal_id)})
     flash("Meal deleted successfully!", category="success")
     return redirect(url_for('main.manage_meals'))


