from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, SelectField
from wtforms.validators import Length, EqualTo, InputRequired, Email, ValidationError
from bank.models import User

def validate_username(self, username_to_check):
    user = User.cursor(username=username_to_check.data).first()
    if user:
        raise ValidationError("Username already exists! Please try a different username")

class RegisterForm(FlaskForm):
    name = StringField(label="Name : ", validators=[InputRequired(), Length(min=2, max=30)])
    gender = SelectField(label="Gender : ", validators=[InputRequired()], choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    dob = DateTimeField(label="Date of Birth : ", validators=[InputRequired()], format="%Y-%m-%d")
    email_address = StringField(label="Email Address: ", validators=[InputRequired(), Email()])
    mobile = StringField(label="Mobile Number : ", validators=[InputRequired(), Length(min=10, max=13)])
    password1 = PasswordField(label="Password : ", validators=[InputRequired(), Length(min=8)])
    password2 = PasswordField(label="Confirm Password : ", validators=[InputRequired(), EqualTo('password1')])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    mobile = StringField(label="Mobile Number : ", validators=[InputRequired()])
    password = PasswordField(label="Password : ", validators=[InputRequired()])
    submit = SubmitField(label="Sign In")

class DepositForm(FlaskForm):
    cash = IntegerField(label="Amount : ", validators=[InputRequired()])
    submit = SubmitField(label="Cash Deposit")


class WithdrawalForm(FlaskForm):
    cash = IntegerField(label="Amount : ", validators=[InputRequired()])
    submit = SubmitField(label="Cash Withdrawal")


class TransferForm(FlaskForm):
    recipient = StringField(label="Recipients Mobile : ", validators=[InputRequired()])
    cash = IntegerField(label="Amount : ", validators=[InputRequired()])
    submit = SubmitField(label="Transfer")
