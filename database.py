from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Factory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    supply = db.Column(db.Integer, nullable=False)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    demand = db.Column(db.Integer, nullable=False)

class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, nullable=False)
    to_id = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "factory_to_warehouse" or "warehouse_to_store"
