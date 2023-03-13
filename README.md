# FlaskUserAuthSystem

[//]: # (This is a simple Flask User Authentication System. It uses Flask-SQLAlchemy for database management and SQLite for database. It uses Flask-Login for user session management. It uses Flask-WTF for form handling. It uses Flask-Bootstrap for styling. It uses Flask-Gravatar for user profile picture. It uses Flask-Mail for sending emails. It uses Flask-Script for running the application. It uses Flask-Migrate for database migrations. It uses Flask-DebugToolbar for debugging. It uses Flask-Testing for testing.)

## Setting up

To set up the application, you need to have [Python 3.11](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/#installation) installed on your system.

After installing Python and Poetry, you need to clone the repository.

```bash
git clone https://github.com/LagrangeH/FlaskUserAuthSystem.git
```

After cloning the repository, you need to create virtual environment.

```bash
poetry env use python3.11
```
After creating the virtual environment, you need to install the dependencies.

```bash
poetry install
```

After installing the dependencies, you need to run the application.

```bash
poetry run flask run
```