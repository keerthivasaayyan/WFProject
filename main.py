from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rainbow_table.db'
app.config['SECRET_KEY'] = 'ASDFGFEJNNEJDNJKEWNIWF'

db = SQLAlchemy(app)

class RainbowTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    plaintext_password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"RainbowTable(id={self.id}, password_hash='{self.password_hash}', plaintext_password='{self.plaintext_password}')"

with app.app_context():
    db.create_all()

import hashlib
from flask import request, jsonify

@app.route('/check', methods=['GET', 'POST'])
def index():
    hash_value = request.args.get('hash')
    result = RainbowTable.query.filter_by(password_hash=hash_value).first()
    if result:
        plaintext_password = result.plaintext_password
        response = {"message": f"The plaintext password for the hash '{hash_value}' is: {plaintext_password}"}
    else:
        response = {"message": f"Sorry, the hash '{hash_value}' was not found in the rainbow table."}
    return jsonify(response)

@app.route('/add', methods=['GET', 'POST'])
def add_password():
    try:
        passw = request.args.get('pass')
        password_hash = hashlib.sha256(passw.encode()).hexdigest()
        result = RainbowTable.query.filter_by(password_hash=password_hash).first()
        if result:
            response = {"message": "Password already exists"}
        else:
            new_entry = RainbowTable(password_hash=password_hash, plaintext_password=passw)
            db.session.add(new_entry)
            db.session.commit()
            response = {"message": "Password Added"}
    except Exception as e:
        response = {"message": "Failed to add Password"}
    return jsonify(response)

@app.route('/view_table')
def view_table():
    entries = RainbowTable.query.all()
    return render_template('view_table.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)