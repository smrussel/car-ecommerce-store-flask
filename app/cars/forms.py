from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_ckeditor import CKEditorField


class ReviewForm(FlaskForm):
    rating = DecimalField(default=0.0, validators=[NumberRange(min=0, max=5)])
    text = CKEditorField("Write a review", validators=[DataRequired()])
    submit = SubmitField('Submit Review')
