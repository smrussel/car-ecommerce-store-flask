from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextField,
                     SelectField, IntegerField)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from datetime import datetime
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Email

country_choice = (
    ('Scotland', 'Scotland'),
    ('Wales', 'Wales'),
    ('England', 'England'),
    ('Northern Ireland', 'Northern Ireland'),
)

admin_choice = (
    (1, 'Admin'),
    (0, 'Customer'),
)

city_choice = (
    ('Aberdeen', 'Aberdeen'),
    ('Armagh', 'Armagh'),
    ('Bath', 'Bath'),
    ('Belfast', 'Belfast'),
    ('Birmingham', 'Birmingham'),
    ('Bradford', 'Bradford'),
    ('Brighton and Hove', 'Brighton and Hove'),
    ('Bristol', 'Bristol'),
    ('Cambridge', 'Cambridge'),
    ('Canterbury', 'Canterbury'),
    ('Cardiff', 'Cardiff'),
    ('Carlisle', 'Carlisle'),
    ('Chelmsford', 'Chelmsford'),
    ('Chester', 'Chester'),
    ('Chichester', 'Chichester'),
    ('Coventry', 'Coventry'),
    ('Derby', 'Derby'),
    ('Dundee', 'Dundee'),
    ('Durham', 'Durham'),
    ('Edinburgh', 'Edinburgh'),
    ('Ely', 'Ely'),
    ('Exeter', 'Exeter'),
    ('Glasgow', 'Glasgow'),
    ('Gloucester', 'Gloucester'),
    ('Hereford', 'Hereford'),
    ('Inverness', 'Inverness'),
    ('Kingston upon Hull', 'Kingston upon Hull'),
    ('Lancaster', 'Lancaster'),
    ('Leeds', 'Leeds'),
    ('Leicester', 'Leicester'),
    ('Lichfield', 'Lichfield'),
    ('Lincoln', 'Lincoln'),
    ('Lisburn', 'Lisburn'),
    ('Liverpool', 'Liverpool'),
    ('London', 'London'),
    ('Londonderry', 'Londonderry'),
    ('Manchester', 'Manchester'),
    ('Newcastle upon Tyne', 'Newcastle upon Tyne'),
    ('Newport', 'Newport'),
    ('Newry', 'Newry'),
    ('Norwich', 'Norwich'),
    ('Nottingham', 'Nottingham'),
    ('Oxford', 'Oxford'),
    ('Perth', 'Perth'),
    ('Peterborough', 'Peterborough'),
    ('Plymouth', 'Plymouth'),
    ('Portsmouth', 'Portsmouth'),
    ('Preston', 'Preston'),
    ('Ripon', 'Ripon'),
    ('Salford', 'Salford'),
    ('Salisbury', 'Salisbury'),
    ('Sheffield', 'Sheffield'),
    ('Southampton', 'Southampton'),
    ('St Albans', 'St Albans'),
    ('St Asaph (Llanelwy)', 'St Asaph (Llanelwy)'),
    ('St Davids', 'St Davids'),
    ('Stirling', 'Stirling'),
    ('Stoke-on-Trent', 'Stoke-on-Trent'),
    ('Sunderland', 'Sunderland'),
    ('Swansea', 'Swansea'),
    ('Truro', 'Truro'),
    ('Wakefield', 'Wakefield'),
    ('Wells', 'Wells'),
    ('Westminster', 'Westminster'),
    ('Winchester', 'Winchester'),
    ('Wolverhampton', 'Wolverhampton'),
    ('Worcester', 'Worcester'),
    ('York', 'York'),
)

year_choice = []
for r in range(2000, (datetime.now().year + 1)):
    year_choice.append((r, r))


class CarForm(FlaskForm):
    car_title = StringField("Title", validators=[DataRequired()])
    country = SelectField('Country', choices=country_choice, validators=[DataRequired()])
    city = SelectField("City", choices=city_choice, validators=[DataRequired()])
    color = StringField("Color", validators=[DataRequired()])
    make = StringField("Make", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    reg_no = StringField("Registration No", validators=[DataRequired()])
    year = SelectField('Year', choices=year_choice, validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    gearbox = StringField("Gearbox", validators=[DataRequired()])
    description = TextField("Description", validators=[DataRequired()])
    car_photo = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    car_photo_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    car_photo_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    car_photo_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    car_photo_4 = FileField('Image 4', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    miles = IntegerField("Miles", validators=[DataRequired()])
    mileage = IntegerField("Mileage", validators=[DataRequired()])
    fuel_type = StringField("Fuel Type", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = FileField('Featured Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FaqForm(FlaskForm):
    question = TextField("Question", validators=[DataRequired()])
    answer = TextField("Answer", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    admin = SelectField("Role", choices=admin_choice, validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

