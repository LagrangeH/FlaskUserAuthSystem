from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField


class RecaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField()
