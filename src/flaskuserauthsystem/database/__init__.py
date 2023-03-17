from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy


@dataclass(frozen=True)
class DB:
    obj = SQLAlchemy()
