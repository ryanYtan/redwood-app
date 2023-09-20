from flask_sqlalchemy import SQLAlchemy
import dataclasses

db = SQLAlchemy()

@dataclasses.dataclass
class User(db.Model):
    username: str = db.Column(db.String(255), primary_key=True)
    hashed_pw: str = db.Column(db.String(1024))

@dataclasses.dataclass
class Item(db.Model):
    item_id: str = db.Column(db.String(255), primary_key=True)
    seller: str = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    name: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.String())
    imetadata: str = db.Column(db.String())
    price: float = db.Column(db.Numeric(10, 2), nullable=False)

@dataclasses.dataclass
class Transaction(db.Model):
    buyer: str = db.Column(db.String(255), primary_key=True)
    item_id: str = db.Column(db.String(255), primary_key=True)
