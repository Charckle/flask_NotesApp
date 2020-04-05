# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import BooleanField, StringField, TextAreaField, PasswordField, HiddenField, SubmitField, validators # BooleanField

# Import Form validators
from wtforms.validators import Email, EqualTo, ValidationError

from app.main_page_module.models import User

#email verification
import re
import os.path


# Define the login form (WTForms)

class EditEntryForm(FlaskForm):

    entry_text = TextAreaField('Entry Text', [validators.InputRequired(message='You need to fill something.')])
    
    submit = SubmitField('Submit changes')
    
class EntryForm(FlaskForm):
    name = StringField('Name of new entry', [validators.InputRequired(message='You need to specify a name'),
                                             validators.Length(max=128)])
    entry_text = TextAreaField('Entry Text', [validators.InputRequired(message='You need to fill something.')])
    
    submit = SubmitField('Add Entry')
    
    def validate_name(self, name):
        
        #check if there is another entry with the same name
        name = str(name.data).strip().replace(' ', '_') 
        name = re.sub(r'(?u)[^-\w.]', '', name)
        
        storage_location = "app//main_page_module//data//"
        files = []
        # r=root, d=directories, f = files
        for _, _, f in os.walk(storage_location):
            for file in f:
                if '.txt' in file:
                    files.append(file)  
        
        if name+".txt" in files:
            raise ValidationError('Entry already exists. Please use a different name for the entry')     
      

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', [validators.InputRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [validators.InputRequired(message='Must provide a password.')])
    remember = BooleanField()
    
    submit = SubmitField('Login')

class EditUserForm(FlaskForm):

    id = HiddenField('id', [validators.InputRequired(message='Dont fiddle around with the code!')])
    name   = StringField('Name', [validators.InputRequired(message='We need a name for the user.')])
    email    = StringField('Email', [validators.InputRequired(message='We need an email for your account.')])
    password  = PasswordField('Password')    
    password_2 = PasswordField('Repeat password', [EqualTo('password', message='Passwords must match')])
      
    submit = SubmitField('Submit changes')
    

class RegisterForm(FlaskForm):
    username   = StringField('Username', [validators.InputRequired(message='We need a username for your account.')])
    email    = StringField('Email', [validators.InputRequired(message='We need an email for your account.')])
    password  = PasswordField('Password')    
    password_2 = PasswordField('Repeat password', [validators.InputRequired(), EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Register')
    
    #When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators and invokes them in addition to the stock validators
    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        
        #check if it is a real email
        if(re.search(regex,email.data)):  
            #if it is, check if there is another user with the same email
            user = User.query.filter_by(email=email.data).first()
        
            if user is not None:
                raise ValidationError('Please use a different email address.')     
        
        else:  
            raise ValidationError('Please use a valid email address.')          
        
        
