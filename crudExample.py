from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug import secure_filename
from pandas import pandas as pd
import sqlite3
import os
import numpy as np




app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'myDB.sqlite')
db = SQLAlchemy(app)
marshmallowApp = Marshmallow(app)



class Input(db.Model): #phase1 table
    key = db.Column(db.Integer, primary_key=True)
    fileType = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, key, fileType, description, email):
        self.key = key
        self.fileType = fileType
        self.description = description
        self.email = email

class Parsed(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    fileType = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)
    name = db.Column(db.String(80), unique=False)
    age = db.Column(db.Integer, unique=False)
    nationality = db.Column(db.String(80), unique=False)
    creditScore = db.Column(db.Integer, unique=False)

    def __init__(self, key, fileType,description,email,name,age,nationality,creditScore):
        self.key = key
        self.fileType = fileType
        self.description = description
        self.email = email
        self.name = name
        self.age = age
        self.nationality = nationality
        self.creditScore = creditScore

class InputSchema(marshmallowApp.Schema):
    class Meta:
        fields = ('key' ,'fileType', 'description', 'email')
class ParsedSchema(marshmallowApp.Schema):
    class Meta:
        fields = ('key' ,'fileType', 'description', 'email','name','age','nationality','creditScore')


input_schema = InputSchema()
inputMulti_schema = InputSchema(many=True)

parsed_schema = ParsedSchema()
parsedMulti_schema = ParsedSchema(many=True)



def convert(val):
    return np.int16(val).item()

@app.route("/input", methods=["POST"])
def add_input():
    key = request.json['key']
    fileType = request.json['fileType']
    description = request.json['description']
    email = request.json['email']
    
    new_input = Input(key, fileType, description, email)

    db.session.add(new_input)
    db.session.commit()

    return input_schema.jsonify(new_input)

@app.route("/input", methods=["GET"])
def get_input():
    all_inputs = Input.query.all()
    result = inputMulti_schema.dump(all_inputs)
    return jsonify(result.data)


@app.route("/input/<key>", methods=["GET"])
def input_detail(key):
    input = Input.query.get(key)
    return input_schema.jsonify(input)


@app.route("/input/<key>", methods=["PUT"])
def input_update(key):
    input = Input.query.get(key)
    fileType = request.json['fileType']
    description = request.json['description']
    email = request.json['email']

    input.fileType = fileType
    input.description = description
    input.email = email

    db.session.commit()
    return input_schema.jsonify(input)


@app.route("/input/<key>", methods=["DELETE"])
def input_delete(key):
    input = Input.query.get(key)
    db.session.delete(input)
    db.session.commit()

    return ("deleted record " + key)

@app.route("/upload", methods=["POST"])
def add_upload():
    f = request.files['file']
    filename = f.filename
    keyValue,filetypeValue = filename.split(".")

    conn = sqlite3.connect("myDB.sqlite")
    cur = conn.cursor()
    print(filetypeValue)
    cur.execute("SELECT * FROM input WHERE key=? and fileType=?",(keyValue,filetypeValue,))
    rows = cur.fetchall()
    if (len(rows)) == 0:
        return ("file does not match our data, disregarding it.")
    else:
        df = pd.read_csv(f.stream)
        x,y,descValue,emailValue = rows[0]
        new_input = Parsed(keyValue, filetypeValue, descValue,emailValue,df.get_value(0,'name'),convert(df.get_value(0,'age')),df.get_value(0,'nationality'),convert(df.get_value(0,'creditScore')))
        db.session.add(new_input)
        oldInput = Input.query.get(keyValue)
        db.session.delete(oldInput)
        db.session.commit()
        
    return ('file uploaded successfully')

@app.route("/upload/<key>", methods=["GET"])
def upload_detail(key):
    parsed = Parsed.query.get(key)
    return parsed_schema.jsonify(parsed)

@app.route("/upload", methods=["GET"])
def get_uploads():
    all_inputs = Parsed.query.all()
    result = parsedMulti_schema.dump(all_inputs)
    return jsonify(result.data)

if __name__ == '__main__':
    app.run(debug=True)


