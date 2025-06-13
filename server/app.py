#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    
    if quake:
        return jsonify({
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "year": quake.year
        })
    else:
        return {"message": f"Earthquake {id} not found."}, 404


@app.route('/earthquakes/magnitude/<float:magnitude>')
def quakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes_data = [{
        "id": q.id,
        "magnitude": q.magnitude,
        "location": q.location,
        "year": q.year
    } for q in quakes]
    
    return jsonify({
        "count": len(quakes),
        "quakes": quakes_data
    })


if __name__ == '__main__':
    app.run(port=5555, debug=True)