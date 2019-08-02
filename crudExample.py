from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'myDB.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=False)
    lastName = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    homeCountry = db.Column(db.String(100), unique=False)
    age = db.Column(db.Integer, unique=False)


    def __init__(self, firstName, lastName, email, homeCountry, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.homeCountry = homeCountry
        self.age = age


class InputSchema(ma.Schema):
    class Meta:
        fields = ('firstName', 'lastName', 'email','homeCountry','age')


input_schema = InputSchema()
inputs_schema = InputSchema(many=True)

@app.route("/input", methods=["POST"])
def add_input():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    homeCountry = request.json['homeCountry']
    age = request.json['age']
    
    new_input = Input(firstName, lastName, email, homeCountry,age)

    db.session.add(new_input)
    db.session.commit()

    return input_schema.jsonify(new_input)


@app.route("/input", methods=["GET"])
def get_input():
    all_inputs = Input.query.all()
    result = inputs_schema.dump(all_inputs)
    return jsonify(result.data)


@app.route("/input/<id>", methods=["GET"])
def input_detail(id):
    input = Input.query.get(id)
    return input_schema.jsonify(input)


@app.route("/input/<id>", methods=["PUT"])
def input_update(id):
    input = Input.query.get(id)
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    homeCountry = request.json['homeCountry']
    age = request.json['age']

    input.firstName = firstName
    input.lastName = lastName
    input.email = email
    input.homeCountry = homeCountry
    input.age = age

    db.session.commit()
    return input_schema.jsonify(input)


@app.route("/input/<id>", methods=["DELETE"])
def input_delete(id):
    input = Input.query.get(id)
    db.session.delete(input)
    db.session.commit()

    return input_schema.jsonify(input)


if __name__ == '__main__':
    app.run(debug=True)