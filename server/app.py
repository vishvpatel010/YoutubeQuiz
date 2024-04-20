from flask import Flask
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime
import hashlib
import urllib

app = Flask(__name__)
jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = '38dd56f56d405e02ec0ba4be4607eaab'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token

client = MongoClient("mongodb://localhost:27017")
db = client["YoutubeQuiz"]

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if db.users.find_one({'email': email}):
            return jsonify({'error': 'Username already exists'}), 400
        new_user = {'name':name, 'email': email, 'password': password}
        db.users.insert_one(new_user)
        return jsonify({'message': 'Signup successful'}), 201
    else:
        return 'Please login.'
    
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get email and password from request data
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Query MongoDB to find user
        user = db.users.find_one({'email': email})

        if user:
            # Check if passwords match
            if user['password'] == password:

                access_token = create_access_token(identity=user['email'])
                return jsonify({'access_token': access_token})
            else:
                # Incorrect password
                return jsonify({'error': 'Incorrect password'}), 401
        else:
            # User not found
            return jsonify({'error': 'User not found'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500
    
if __name__ == '__main__':
    app.run(debug=True,port=8080)