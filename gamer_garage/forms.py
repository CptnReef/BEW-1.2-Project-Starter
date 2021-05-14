from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from .models import GamerGarage, GameSelection, ImageSelection, User

class GameGarageForm(FlaskForm):
    """Form for adding/updating a Gamer Garage."""

    title = StringField('Title')
    address = StringField('Address')
    submit_button = SubmitField('Submit')

class GameItemForm(FlaskForm):
    """Form for adding/updating a GameItem."""
    
    name = SelectField(choices=[(x.name, x.value) for x in GameSelection])
    price = FloatField('Price')
    store = QuerySelectField(query_factory=lambda: GamerGarage.query, allow_blank=False, get_label='title')
    submit_button = SubmitField('Submit')


class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
