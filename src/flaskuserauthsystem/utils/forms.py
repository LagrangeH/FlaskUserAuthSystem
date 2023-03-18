from flask_wtf import FlaskForm, RecaptchaField


class RecaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
