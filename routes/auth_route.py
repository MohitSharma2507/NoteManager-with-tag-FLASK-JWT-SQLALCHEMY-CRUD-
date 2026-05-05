from flask import Blueprint,session,request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from werkzeug.security import generate_password_hash,check_password_hash
from models import User,db

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data or not data.get('email') or not data.get('password') :
        return jsonify({
            'error':'Email and password are required'
        }),400
    
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password ,password):
        return jsonify({
            'error':'Invalid email or password'
        }),400
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message':'Login Successful',
        'access_token':access_token,
        'user':user.to_dict()
    }),200
    
@auth_bp.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    if not data or not data.get('email') or not data.get('password') :
        return jsonify({
            'error':'Email and password are required'
        }),400
    
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            'error':'User Already exist'
        }),409
    
    if len(password) < 8:
        return jsonify({
            'error':'Password must be more than 8 char'
        }),400
    
    hash_password = generate_password_hash(password)
    user  = User(email=email,password=hash_password)

    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message':'Signup Successfull',
        'user':user.to_dict()
    }),201