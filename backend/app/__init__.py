from flask import Flask,request, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import User, Trek, Booking, StaffProfile


db = SQLAlchemy()

jwt = JWTManager()



def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)

    jwt.init_app(app)
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(role="admin").first()

        if not admin:
            admin = User(
                name="Admin",
                email="admin@gmail.com",
                role="admin",
                phone="9999999999",
                is_active=True
            )

            admin.set_password("admin123")

            db.session.add(admin)
            db.session.commit()

    @app.route("/")
    def home():
        return "Welcome to Trekking Management API"

    @app.route("/register", methods=["POST"])
    def register():

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        # Check if any required field is missing
        if not name or not email or not password:
            return jsonify({
                "message": "Name, email and password are required."
            }), 400

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "message": "Email already registered."
            }), 409

        # Create new user
        user = User(
            name=name,
            email=email,
            role="user",
            phone=phone
        )

        # Hash password
        user.set_password(password)

        # Save to database
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful.",
            "user_id": user.id
        }), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email  = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({
                "message": "Email and password are required."
            }), 400
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({
                "message": "Invalid email or password."
            }), 401
        #checking account status
        if not user.is_active:
            return jsonify({
                "message": "Account is inactive. Please contact support."
            }), 403
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "role"  : user.role,
            "name": user.name
        }), 200
    
    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def profile():

        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }), 200




    return app

