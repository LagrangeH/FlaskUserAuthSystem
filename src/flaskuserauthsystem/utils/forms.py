from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RecaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
