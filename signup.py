from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password.crwa8q8k0lvn.ap-south-1.rds.amazonaws.com/signup'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Signup(db.Model):
    __tablename__ = 'signup'
    name = db.Column(db.String(50))
    mobile = db.Column(db.String(10))
    email = db.Column(db.String(50), primary_key=True)
    passwords = db.Column(db.String(1000))
    organization = db.Column(db.String(1000))
    description = db.Column(db.String(1000))

@app.route('/')
def index():
    signups = Signup.query.all()
    result = "<br>".join([f"Email: {signup.email}, Password: {signup.passwords}" for signup in signups])
    return result

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400
    
    email = data.get("email")
    password = data.get("passwords")
    name = data.get("name")
    mobile = data.get("mobile")
    organization = data.get("organization")
    description = data.get("description")

    existing_user = Signup.query.get(email)
    if existing_user:
        return jsonify({"error": "User with email already exists"}), 409

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = Signup(email=email, passwords=hashed_password, name=name, mobile=mobile, organization=organization, description=description)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    data = request.json
    new_password = data.get("passwords")
    name = data.get("name")
    mobile = data.get("mobile")
    organization = data.get("organization")
    description = data.get("description")

    if not new_password:
        return jsonify({"error": "Invalid request, new_password missing"}), 400

    user = Signup.query.get(email)
    if not user:
        return jsonify({"error": f"User with email {email} not found"}), 404

    hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
    user.passwords = hashed_password
    user.name = name
    user.mobile = mobile
    user.organization = organization
    user.description = description
    db.session.commit()

    return jsonify({"message": "User details updated successfully"}), 200

@app.route('/delete/<email>', methods=['DELETE'])
def delete_user(email):
    user = Signup.query.get(email)
    if not user:
        return jsonify({"error": f"User with email {email} not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User with email {email} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
