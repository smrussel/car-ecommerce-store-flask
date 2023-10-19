from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class CarReserveForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField("Submit")

