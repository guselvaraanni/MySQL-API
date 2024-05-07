from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@motormojo.crwa8q8k0lvn.ap-south-1.rds.amazonaws.com/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'
    email = db.Column(db.String(50), primary_key=True)
    passwords = db.Column(db.String(100)) 



@app.route('/')
def index():
    logins = Login.query.all()
    
    result = "<br>".join([f"Email: {login.email}, Password: {login.passwords}" for login in logins])
    
    return result


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400
    
    email = data.get("email")
    password = data.get("passwords")

    existing_user = Login.query.get(email)
    if existing_user:
        return jsonify({"error": "User with email already exists"}), 409

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = Login(email=email, passwords=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    email = data.get("email")
    Entered_password = data.get("passwords")

    user = Login.query.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if Entered_password is None:
        return jsonify({"error": "Password is missing"}), 401

    hashed_password_entered = hashlib.sha256(Entered_password.encode('utf-8')).hexdigest()
    hashed_password_stored = user.passwords
    print(hashed_password_stored)
    print(hashed_password_entered)

    if hashed_password_entered == hashed_password_stored:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    data = request.json
    new_password = data.get("passwords")

    if not new_password:
        return jsonify({"error": "Invalid request, new_password missing"}), 400

    user = Login.query.get(email)
    if not user:
        return jsonify({"error": f"User with email {email} not found"}), 404

    hashed_password = sha256(new_password.encode('utf-8')).hexdigest()
    user.passwords = hashed_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

@app.route('/delete/<email>', methods=['DELETE'])
def delete_user(email):
    user = Login.query.get(email)
    if not user:
        return jsonify({"error": f"User with email {email} not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User with email {email} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
