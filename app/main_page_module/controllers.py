# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
# Import the database object from the main app module
from app import db

# Import module forms
from app.main_page_module.forms import LoginForm, RegisterForm, EntryForm, EditEntryForm, EditUserForm

# Import module models (i.e. User)
from app.main_page_module.models import User
#import os
import re
import os

from app.main_page_module.argus import WSearch

# Define the blueprint: 'auth', set its url prefix: app.url/auth
main_page_module = Blueprint('main_page_module', __name__, url_prefix='/')

#login check
def check_login():
    if "user_id" not in session:
        return True
        
    
# Set the route and accepted methods
@main_page_module.route('/', methods=['GET', 'POST'])
def index():
    if check_login(): return redirect(url_for("main_page_module.login"))  

    return render_template("main_page_module/index.html")

@main_page_module.route('/search/', methods=['POST'])
def searc_results():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    key = request.form["key"]
    
    banana = WSearch()
    if key == "":
        asterix = ""
    else:
        asterix = "*"
    res = banana.index_search(key + asterix)    

    results = {str(r[0][29:-4]).strip().replace('_', ' ').capitalize(): [str(r[0][29:-4]).strip(), r[1]] for r in res}
    
    #print(results)
    return jsonify(results)

@main_page_module.route('/delete/', methods=['POST'])
def delete_entry():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    entry_id = request.form["id"]
    name = str(entry_id).strip().replace(' ', '_')
    
    banana = f"app//main_page_module//data//{name}.txt"
    if os.path.exists(banana):
        os.remove(banana)
        
        #update argus index
        new_index = WSearch()
        new_index.index_create()        
        
        flash('Entry successfully deleted.', 'success')
        
        return redirect(url_for("main_page_module.index"))      
      
    else:
        flash('No entries with this name found to delete.', 'error')
        
        return redirect(url_for("main_page_module.index"))        


@main_page_module.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    # If sign in form is submitted
    form = EntryForm(request.form)
    
    # Verify the sign in form
    if form.validate_on_submit():
        name = str(form.name.data).strip().replace(' ', '_') 
        name = re.sub(r'(?u)[^-\w.]', '', name)        
        new_filename = "app//main_page_module//data//" + name + ".txt"
        #print(os.getcwd())
        with open(f'{new_filename}', 'w') as file:
                file.write(form.entry_text.data)
        
        #create argus index
        new_index = WSearch()
        new_index.index_create()
        
        flash('Entry successfully created!', 'success')
        flash('Argus index successfully updated', 'success')
        
        return redirect(f"view_entry/{name}")
        #return redirect(url_for("main_page_module.view_entry"), entry_name=new_filename)

    return render_template("main_page_module/new_entry.html", form=form)

@main_page_module.route('/all_entry/')
def all_entry():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    storage_location = "app//main_page_module//data//"
    
    files = []
    # r=root, d=directories, f = files
    for _, _, f in os.walk(storage_location):
        for file in f:
            if '.txt' in file:
                name_for_link = str(file).strip().replace(' ', '_')[:-4]
                files.append([os.path.join(storage_location, file), file[:-4].replace('_', ' ').capitalize(), name_for_link])

   
    return render_template("main_page_module/all_entry.html", files=files)

@main_page_module.route('/view_entry/<entry_name>', methods=['GET', 'POST'])
def view_entry(entry_name):
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    title = str(entry_name).strip().replace('_', ' ').capitalize()
    text = ""
    
    try:
        banana = f"app//main_page_module//data//{entry_name}.txt"
        #http://127.0.0.1:5000/view_entry/apre_ticket
        with open(banana, 'r') as file:
            
            text = file.read()

    except:
        flash('No entries with this name found', 'error')
        
        return redirect(url_for("main_page_module.index"))

    print(entry_name)
    return render_template("main_page_module/view_entry.html", entry_name=title, entry_text=text, link_entry_name=entry_name)

@main_page_module.route('/edit_entry/<entry_name>', methods=['GET', 'POST'])
def edit_entry(entry_name):
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    title = str(entry_name).strip().replace('_', ' ').capitalize()
    text = ""
    banana = f"app//main_page_module//data//{entry_name}.txt"
    form = EditEntryForm(request.form)
    #verify if the file exists
    if not os.path.exists(banana):
        flash('No entries with this name found ' + f"view_entry/{entry_name}", 'error')
        
        return redirect(url_for("main_page_module.index"))
    
    # Verify the sign in form
    if form.validate_on_submit():
        with open(banana, 'w') as file:
            #print(repr(form.entry_text.data))
            escaped_text = form.entry_text.data.replace("\r", "")
            file.write(escaped_text)
        
        #create argus index
        new_index = WSearch()
        new_index.index_create()
        
        flash('Entry successfully Eddited!', 'success')
        flash('Argus index successfully updated', 'success')
        
        #return redirect(f"/view_entry/{entry_name}")
        return redirect(url_for("main_page_module.view_entry", entry_name=entry_name))
        #return redirect(url_for("main_page_module.view_entry"), entry_name=new_filename)
    else:
        with open(banana, 'r') as file:
            text = file.read()
            #print(repr(text))

    return render_template("main_page_module/edit_entry.html", entry_name=title, entry_text=text, link_entry_name=entry_name, form=form)

        
@main_page_module.route('/admin/all_users/')
def all_users():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    users = User.query.all()
   
    return render_template("main_page_module/admin/all_users.html", users=users)


@main_page_module.route('/admin/view_user/<user_id>')
def view_user(user_id):
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    user = User.query.filter_by(id=user_id).first()
   
    if not user:
        flash('User does not exist.', 'error')
        
        return redirect(url_for("main_page_module.all_users"))     
    
    form = EditUserForm()
    form.process(obj=user)
    
   
    return render_template("main_page_module/admin/view_user.html", form=form, user=user)

@main_page_module.route('/admin/modify_user/', methods=['POST'])
def modify_user():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    form = EditUserForm(request.form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        
        if not user:
            flash('User does not exist.', 'error')
        
            return redirect(url_for("main_page_module.all_users")) 
        
        else:
            user.name =  form.name.data
            user.email =  form.email.data
            if form.password.data != "":
                user.set_password(form.password.data)
    
            db.session.commit()   
        
        flash('User successfully Eddited!', 'success')
        
        return redirect(url_for("main_page_module.view_user", user_id=form.id.data, form=form))
    
    flash('Invalid data.', 'error')

    return redirect(url_for("main_page_module.all_users"))     
    

@main_page_module.route('/admin/delete/', methods=['POST'])
def delete_user():
    if check_login(): return redirect(url_for("main_page_module.login"))  
    
    user_id = request.form["id"]
    
    user = User.query.filter_by(id=user_id).first()
   
    if not user:
        flash('User does not exist.', 'error')
        
        return redirect(url_for("main_page_module.all_users")) 
    
    else:
        db.session.delete(user)
        db.session.commit()        
        
        flash(f'User {user.name} - {user.username} successfully deleted.', 'success')
        
        return redirect(url_for("main_page_module.all_users")) 
    

# Set the route and accepted methods
@main_page_module.route('/login/', methods=['GET', 'POST'])
def login():

    # If sign in form is submitted
    form = LoginForm(request.form)
    
    

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username_or_email.data).first()
        if not user:
            user = User.query.filter_by(email=form.username_or_email.data).first()

        if user and user.check_password(form.password.data):

            session['user_id'] = user.id
            
            #set permanent login, if selected
            if form.remember.data == True:
                session.permanent = True

            flash('Welcome %s' % user.name, 'success')
            
            return redirect(url_for('main_page_module.index'))

        flash('Wrong email or password', 'error')
    
    try:
        if(session['user_id']):
            return redirect(url_for("main_page_module.index"))
    
    except:
        return render_template("main_page_module/auth/login.html", form=form)

@main_page_module.route('/logout/')
def logout():
    session.pop("user_id", None)
    session.permanent = False
    
    flash('You have been logged out. Have a nice day!', 'success')

    return redirect(url_for("main_page_module.login"))

# Set the route and accepted methods
@main_page_module.route('/register/', methods=['GET', 'POST'])
def register():
    #insert check, if the user is already logged in
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password = form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'success')
        
        return redirect(url_for('main_page_module.login'))
    return render_template('main_page_module/auth/register.html', title='Register', form=form)