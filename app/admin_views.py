from app import app, session
from flask import render_template, request, redirect, url_for, send_from_directory
from app.database import  MenuItem, MenuItemUser, Cheese
import os
from werkzeug.utils import secure_filename

def menu():
    return session.query(MenuItem).all()
def menuUser():
    return session.query(MenuItemUser).all()


@app.route("/admin/edit_menu_element", methods=['GET', 'POST'])
def edit_menu_element():
    if request.method == 'POST':
        MenuItemName = request.form['MenuItemName']
        url = request.form['url']
        item_id = request.form['item_id']
        
        menu_item = session.query(MenuItem).get(item_id)
        menu_item.name = MenuItemName
        menu_item.url = url
        
        try:
            session.commit()
            return redirect('/admin/edit_menu')
        except Exception as e:
            return "Klaida klaidele klaiduzele" + str(e)
    else:
        return render_template("admin/edit_menu.html", menu=menu())
    
@app.route("/admin/add_menu_element", methods=['GET', 'POST'])
def add_menu_element():
    if request.method == 'POST':
        MenuItemName = request.form['MenuItemName']
        url = request.form['url']
        
        menu_item = MenuItem(MenuItemName, url)
        try:
            session.add(menu_item)
            session.commit()
            return redirect('/admin/edit_menu')
        except Exception as e:
            return "Klaida klaidele klaiduzele" + str(e)
    else:
        return render_template("admin/edit_menu.html", menu=menu())
    
@app.route("/admin/edit_menu", methods=['GET', 'POST'])
def edit_menu():
    columns = MenuItem.__table__.columns.keys()
    return render_template("admin/edit_menu.html", menu=menu(), columns=columns)

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', menu=menu())

@app.route('/handle_form', methods=['POST'])
def handle_form():


    item_id = request.form['item_id']
    action = request.form['action']

    menu_item = session.query(MenuItem).get(item_id)
    if action == 'delete':
        try:
            session.delete(menu_item)
            session.commit()
            return redirect('admin/edit_menu')
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            return "klaidelelelelelelel istrinant" + str(e)
        
    
    return redirect(url_for('edit_menu'))

@app.route('/handle_form_user', methods=['POST'])
def handle_form_user():


    item_id = request.form['item_id']
    action = request.form['action']

    menu_item = session.query(MenuItemUser).get(item_id)
    if action == 'delete':
        try:
            session.delete(menu_item)
            session.commit()
            return redirect('admin/edit_menu_user')
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            return "klaidelelelelelelel istrinant" + str(e)
        
    
    return redirect(url_for('edit_menu'))
@app.route("/admin/edit_menu_element_user", methods=['GET', 'POST'])
def edit_menu_element_user():
    if request.method == 'POST':
        MenuItemName = request.form['MenuItemName']
        url = request.form['url']
        item_id = request.form['item_id']
        
        menu_item = session.query(MenuItemUser).get(item_id)
        menu_item.name = MenuItemName
        menu_item.url = url
        
        try:
            session.commit()
            return redirect('/admin/edit_menu_user')
        except Exception as e:
            return "Klaida klaidele klaiduzele" + str(e)
    else:
        return render_template("admin/edit_menu_user.html", menu=menu())
    
@app.route("/admin/add_menu_element_user", methods=['GET', 'POST'])
def add_menu_element_user():
    if request.method == 'POST':
        MenuItemName = request.form['MenuItemName']
        url = request.form['url']
        
        menu_item = MenuItemUser(MenuItemName, url)
        try:
            session.add(menu_item)
            session.commit()
            return redirect('/admin/edit_menu_user')
        except Exception as e:
            return "Klaida klaidele klaiduzele" + str(e)
    else:
        return render_template("admin/edit_menu_user.html", menu=menu())
    
@app.route("/admin/edit_menu_user", methods=['GET', 'POST'])
def edit_menu_user():
    columns = MenuItemUser.__table__.columns.keys()
    return render_template("admin/edit_menu_user.html", menu=menu(), menuUser=menuUser(), columns=columns)

@app.route('/admin/upload')
def upload():
    return render_template('/admin/upload.html', menu=menu())



@app.route('/admin/add_cheese', methods=['GET', 'POST'])
def add_cheese():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cheese_type = request.form['cheese_type']  
        origin = request.form['origin']
        milk = request.form['milk']
        img_name = request.files['img_name']
        
        if img_name:
            filename = secure_filename(img_name.filename)  
            img_name.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        new_cheese = Cheese(name=name, description=description, cheese_type=cheese_type, origin=origin, milk=milk, img_name=filename)
        session.add(new_cheese)
        session.commit()
        
        return redirect('/admin/add_cheese')  

    return render_template('/admin/add_cheese.html', menu=menu())

@app.route('/admin/edit_galerija', methods=['GET', 'POST'])
def galerija():
    cheeses = session.query(Cheese).all()
    return render_template('/admin/edit_galerija.html', menu=menu(), cheeses=cheeses)

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<int:file_id>')
def download(file_id):
    file = session.query(Cheese).get(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.img_name, as_attachment=True)

@app.route('/delete/<int:file_id>')
def delete(file_id):
    file = session.query(Cheese).get(file_id)
    filename=file.img_name
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    session.delete(file)
    session.commit()
    return redirect("/admin/edit_galerija")

@app.route('/edit/<int:file_id>', methods=['GET', 'POST'])
def edit(file_id):
    file = session.query(Cheese).get(file_id)
    if request.method == 'GET':
        return render_template('/admin/edit_cheese.html', file=file, menu=menu())
    
    elif request.method == 'POST':
        
        new_name = request.form['name']
        new_description = request.form['description']
        new_type = request.form['cheese_type']
        new_origin = request.form['origin']
        new_milk = request.form['milk']
        
        new_img = request.files['new_img_name']
        if new_img:
            
            filename = secure_filename(new_img.filename)
            new_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.img_name = filename
        else:
            filename = file.img_name
        
        file.name = new_name
        file.description = new_description
        file.cheese_type = new_type
        file.origin = new_origin
        file.milk = new_milk
        
        session.commit()
        
        return redirect("/admin/edit_galerija")

