from app import app, session, login_manager
from flask import render_template, redirect, request, flash, url_for, jsonify
from app.database import MenuItemUser, User, Cheese
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user
from app.pytorch_cheese import is_it_cheese
from sqlalchemy import desc

@app.before_request
def require_login():
    # Exclude /sign_in and /sign_up from the login requirement
    if request.endpoint in ['sign_in', 'sign_up', 'static']:
        return

    # Check if the user is authenticated
    if not current_user.is_authenticated:
        # Redirect to the login page and include the 'next' parameter
        return redirect(url_for('sign_in', next=request.url))
    
def menuUser():
    return session.query(MenuItemUser).all()
    
@app.route('/')
def index():
    img_path = 'app/static/images/settings.webp' 
    result = is_it_cheese.predict(img_path)
    return render_template('public/index.html', menu=menuUser(), result=result)

@app.route('/predict', methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({'result': 'No image uploaded'}), 400

    image = request.files['image']
    image_path = 'app/uploads/uploaded_image.jpg'

    if image:
        image.save(image_path)
        result = is_it_cheese.predict(image_path)
        
        if result is not None and result.strip():
            return jsonify({'result': result})

    return jsonify({'result': 'No prediction available'})

@app.route('/what_is_that', methods=["GET", "POST"])
def what_is_that():  
    return render_template('public/what_is_that.html', menu=menuUser())

@app.route('/info')
def info():
    return render_template('public/info.html', menu=menuUser())

@app.route('/galerija', methods=['GET'])
def galerija_public():
    cheeses = session.query(Cheese).all()
    return render_template('public/galerija.html', menu=menuUser(), cheeses=cheeses)

    
@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = session.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))

            else:
                flash("Neteisingi duomenys")
        else:
            flash("Užpildykite laukus")

    return render_template('public/sign_in.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    username= request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if password1 != password2:
            flash("Slaptazodziai nesutampa")
        else:
            hash_password = generate_password_hash(password1)
            newUser = User(username=username, password=hash_password)
            session.add(newUser)
            session.commit()
            return redirect(url_for('index'))

    return render_template('public/sign_up.html')

@app.route('/log_out', methods=["GET", "POST"])
def log_out():
    logout_user()
    return redirect(url_for('sign_in'))

@app.route('/galerija/<int:cheese_id>')
def cheese_details(cheese_id):
    
    selected_cheese = session.query(Cheese).get(cheese_id)

    return render_template('public/cheese_details.html', cheese=selected_cheese, menu=menuUser())
