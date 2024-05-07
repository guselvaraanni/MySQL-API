from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password.crwa8q8k0lvn.ap-south-1.rds.amazonaws.com/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'
    email = db.Column(db.String(50), primary_key=True)
    passwords = db.Column(db.String(100)) 


@app.route('/forget_password/<email>', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
