from datetime import datetime

import bcrypt
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as log

from db_models import User
from db_queries import email_registered, username_registered
from loader import app, db


@app.route('/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        content = request.form.to_dict()

        if (email_raises := email_registered(content['email'])) \
                or (username_raise := username_registered(content['username'])):
            # TODO: return error message
            pass

        password_hash = bcrypt.hashpw(content['pass'].encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=content['username'],
            email=content['email'],
            password_hash=password_hash,
            registration_date=datetime.utcnow(),
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            log.success(f'{new_user} has been registered!')
            return redirect('/')
        except Exception as e:
            log.opt(exception=True).error(e)

    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('/auth/signup.html')


@app.route('/signin')
def signin():
    return render_template('/auth/signin.html')


if __name__ == '__main__':
    app.run(debug=True)
