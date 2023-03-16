from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class _BaseForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')


class SignUpForm(_BaseForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired()])


class SignInForm(_BaseForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class ResetPasswordForm(_BaseForm):
    email = StringField('email', validators=[DataRequired()])


class RestorePasswordForm(_BaseForm):
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired()])
