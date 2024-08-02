from flask import Flask, render_template, jsonify
from database import db, Factory, Warehouse, Store, Cost
from optimization import optimize_supply_chain
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supply_chain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    results = optimize_supply_chain()
    return render_template('index.html', results=results)

@app.route('/data')
def data():
    results = optimize_supply_chain()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
