from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitFieid, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)] )
    email = StringField('Email',
                        validators=[DataRequired(), Email()] )
    password = PasswordField('Password',validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('Password') ])
    submit = SubmitFieid('Sign Up')

class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()] )
    password = PasswordField('Password',validators=[DataRequired()])
    # remember by cookie
    remember = BooleanField('Remember Me')
    submit = SubmitFieid('Login')