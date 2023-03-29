from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Choose a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class JoinGroupForm(FlaskForm):
    group_id = IntegerField('Group ID', validators=[DataRequired()])
    submit = SubmitField('Join Group')

class AddBillForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=200)])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Bill')
    
class JoinGroupForm(FlaskForm):
    group_id = IntegerField('Group ID', validators=[DataRequired()])
    name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Join Group')
