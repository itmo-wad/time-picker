'''
Contains forms for data input as classes, validators for data validation
'''

import mongodb_query
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class MyBaseForm(FlaskForm):
	class Meta:
		locales = ['en']


# Register new user form
class RegistrationForm(MyBaseForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=3, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password',
									  validators=[DataRequired(), EqualTo('password')])
	name = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	phone_number = StringField('Phone', validators=[DataRequired(), Length(min=4, max=16)])
	submit = SubmitField('Sign up')
	
	def validate_username(self, username):
		if mongodb_query.user_exists(username=username.data):
			raise ValidationError('That username is taken. Please choose a different one.')


# Login form
class LoginForm(MyBaseForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Sign in')


# Change settings form
class UpdateAccountForm(MyBaseForm):
	profile_pic = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	phone_number = StringField('Phone', validators=[DataRequired(), Length(min=4, max=16)])
	submit = SubmitField('Update')
	
	def validate_username(self, username):
		if username.data != current_user.username:
			if mongodb_query.user_exists(username=username.data):
				raise ValidationError('That username is taken. Please choose a different one.')


# Search on mainpage form
class MainpageSearchForm(MyBaseForm):
	pass


# Form for adding uslugi of service
class SeviceUslugiForm(MyBaseForm):
	s_name = StringField('Service name', validators=[])
	s_price = StringField('Service price', validators=[])


# Service creation form
class CreateServiceForm(MyBaseForm):
	service_name = StringField('Username', validators=[DataRequired()])
	service_description = TextAreaField('Service description', validators=[DataRequired()])
	service_pic = FileField('Choose service logo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	uslugi = FieldList(FormField(SeviceUslugiForm), min_entries=1, max_entries=32)
	
