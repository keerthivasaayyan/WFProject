from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rainbow_table.db'
db = SQLAlchemy(app)

class RainbowTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    plaintext_password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"RainbowTable(id={self.id}, password_hash='{self.password_hash}', plaintext_password='{self.plaintext_password}')"

def add_entries_from_file(file_path):
    with app.app_context():
        count=0
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                plaintext_password = line
                try:
                    hash_value=hashlib.sha256(line.encode()).hexdigest()
                except:
                    continue
                new_entry = RainbowTable(password_hash=hash_value, plaintext_password=plaintext_password)
                db.session.add(new_entry)
                db.session.commit()
                print(f"added {plaintext_password},{count}")
                count+=1
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_entries_from_file('rockyou.txt')