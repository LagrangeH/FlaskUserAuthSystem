# from datetime import datetime
#
# from faker import Faker
#
# from database import DB
# from database.models import User
#
# fake = Faker()
#
#
# def test_create_user(app):
#     username, email, password = fake.user_name(), fake.email(), fake.password()
#     user = User(username=username, email=email, password_hash=password)
#     print(user, user.__dict__)
#
#     with app.app_context():
#         DB.obj.session.add(user)
#
#     DB.obj.session.commit()
#
#     assert user.id is not None
#     assert user.username is not None
#     assert user.email is not None
#     assert user.password_hash is not None
#     assert user.registration_date <= datetime.utcnow()
