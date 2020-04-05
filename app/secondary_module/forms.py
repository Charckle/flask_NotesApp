# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    username_or_email    = TextField('Username or Email', [Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])

class RegisterForm(Form):
    username   = TextField('Username', [Required(message='We need a username for your account.')])
    email    = TextField('Email', [Email(),
                                               Required(message='We need an email for your account.')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])