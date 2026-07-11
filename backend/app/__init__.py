from flask import Flask,request, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from datetime import datetime

db = SQLAlchemy()

jwt = JWTManager()
from app.models import User, Trek, Booking, StaffProfile


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

    @app.route("/treks", methods=["POST"])
    @jwt_required()
    def create_trek():
     
 
        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"message": "User not found."}), 404
        

        # Only admin can create treks
        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        data = request.get_json()

        name = data.get("name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        duration = data.get("duration")
        available_slots = data.get("available_slots")
        assigned_staff_id = data.get("assigned_staff_id")
        status = data.get("status")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        description = data.get("description")

        # Required fields
        if not all([
            name,
            location,
            difficulty,
            duration,
            available_slots,
            status,
            start_date,
            end_date
        ]):
            return jsonify({
                "message": "Missing required fields."
            }), 400

        # Convert string to Python date
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            assigned_staff_id=assigned_staff_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        db.session.add(trek)
        db.session.commit()

        return jsonify({
            "message": "Trek created successfully.",
            "trek_id": trek.id
        }), 201


    @app.route("/treks", methods=["GET"])
    @jwt_required()
    def get_treks():

        treks = Trek.query.all()

        trek_list = []

        for trek in treks:
            trek_list.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "available_slots": trek.available_slots,
                "assigned_staff_id": trek.assigned_staff_id,
                "staff_name": trek.staff.name if trek.staff else None,
                "status": trek.status,
                "start_date": trek.start_date.strftime("%Y-%m-%d"),
                "end_date": trek.end_date.strftime("%Y-%m-%d"),
                "description": trek.description
            })

        return jsonify(trek_list), 200

    @app.route("/treks/<int:trek_id>", methods=["GET"])
    @jwt_required()
    def get_trek(trek_id):

        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        return jsonify({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "assigned_staff_id": trek.assigned_staff_id,
            "staff_name": trek.staff.name if trek.staff else None,
            "status": trek.status,
            "start_date": trek.start_date.strftime("%Y-%m-%d"),
            "end_date": trek.end_date.strftime("%Y-%m-%d"),
            "description": trek.description
        }), 200

    @app.route("/treks/<int:trek_id>", methods=["PUT"])
    @jwt_required()
    def update_trek(trek_id):

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find trek
        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        data = request.get_json()

        trek.name = data.get("name", trek.name)
        trek.location = data.get("location", trek.location)
        trek.difficulty = data.get("difficulty", trek.difficulty)
        trek.duration = data.get("duration", trek.duration)
        trek.available_slots = data.get("available_slots", trek.available_slots)
        trek.assigned_staff_id = data.get("assigned_staff_id", trek.assigned_staff_id)
        trek.status = data.get("status", trek.status)
        trek.description = data.get("description", trek.description)

        if data.get("start_date"):
            trek.start_date = datetime.strptime(
                data.get("start_date"),
                "%Y-%m-%d"
            ).date()

        if data.get("end_date"):
            trek.end_date = datetime.strptime(
                data.get("end_date"),
                "%Y-%m-%d"
            ).date()

        db.session.commit()

        return jsonify({
            "message": "Trek updated successfully."
        }), 200





    @app.route("/treks/<int:trek_id>", methods=["DELETE"])
    @jwt_required()
    def delete_trek(trek_id):

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find trek
        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404
        if trek.bookings:
            return jsonify({
                "message": "Cannot delete trek with existing bookings."
            }), 400
        # Delete trek
        db.session.delete(trek)
        db.session.commit()

        return jsonify({
            "message": "Trek deleted successfully."
        }), 200


    @app.route("/bookings", methods=["POST"])
    @jwt_required()
    def book_trek():

        # Logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "user":
            return jsonify({
                "message": "Only users can book treks."
            }), 403

        data = request.get_json()

        trek_id = data.get("trek_id")

        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        if trek.available_slots <= 0:
            return jsonify({
                "message": "No slots available."
            }), 400
        
        existing_booking = Booking.query.filter_by(
            user_id=user.id,
            trek_id=trek.id
        ).first()

        if existing_booking:
            return jsonify({
                "message": "You have already booked this trek."
            }), 400
        

        if trek.status != "Open":
            return jsonify({
                "message": "This trek is not open for booking."
            }), 400
        
        booking = Booking(
            user_id=user.id,
            trek_id=trek.id,
            booking_date=datetime.now(),
            status="Booked",
            payment_status="Pending"
        )

        db.session.add(booking)

        trek.available_slots -= 1

        db.session.commit()

        return jsonify({
            "message": "Trek booked successfully.",
            "booking_id": booking.id
        }), 201

    @app.route("/bookings", methods=["GET"])
    @jwt_required()
    def get_bookings():

        user_id = int(get_jwt_identity())

        bookings = Booking.query.filter_by(user_id=user_id).all()

        booking_list = []

        for booking in bookings:
            booking_list.append({
                "booking_id": booking.id,
                "trek_id": booking.trek.id,
                "trek_name": booking.trek.name,
                "assigned_staff_id": booking.trek.assigned_staff_id,
                "staff_name": booking.trek.staff.name if booking.trek.staff else None,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": booking.status,
                "payment_status": booking.payment_status
            })

        return jsonify(booking_list), 200





    @app.route("/staff", methods=["POST"])
    @jwt_required()
    def create_staff():
        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        if not name or not email or not password:
            return jsonify({
                "message": "Name, email and password are required."
            }), 400

        existing = User.query.filter_by(email=email).first()

        if existing:
            return jsonify({
                "message": "Email already exists."
            }), 409

        staff = User(
            name=name,
            email=email,
            role="staff",
            phone=phone,
            is_active=True
        )

        staff.set_password(password)

        db.session.add(staff)
        db.session.commit()

        return jsonify({
            "message": "Staff created successfully.",
            "staff_id": staff.id
        }), 201

    @app.route("/staff", methods=["GET"])
    @jwt_required()
    def get_staff():

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Get all staff users
        staff_members = User.query.filter_by(role="staff").all()

        staff_list = []

        for staff in staff_members:
            staff_list.append({
                "id": staff.id,
                "name": staff.name,
                "email": staff.email,
                "phone": staff.phone,
                "is_active": staff.is_active
            })

        return jsonify(staff_list), 200


    @app.route("/treks/<int:trek_id>/assign-staff", methods=["PUT"])
    @jwt_required()
    def assign_staff(trek_id):

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find trek
        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        data = request.get_json()

        staff_id = data.get("staff_id")

        if not staff_id:
            return jsonify({
                "message": "Staff ID is required."
            }), 400

        # Find staff
        staff = db.session.get(User, staff_id)

        if not staff:
            return jsonify({
                "message": "Staff not found."
            }), 404

        # Check role
        if staff.role != "staff":
            return jsonify({
                "message": "Selected user is not a staff member."
            }), 400

        # Assign staff
        trek.assigned_staff_id = staff.id

        db.session.commit()

        return jsonify({
            "message": "Staff assigned successfully."
        }), 200


    @app.route("/bookings/<int:booking_id>/cancel", methods=["PUT"])
    @jwt_required()
    def cancel_booking(booking_id):

        # Logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "user":
            return jsonify({
                "message": "Only users can cancel bookings."
            }), 403

        # Find booking
        booking = db.session.get(Booking, booking_id)

        if not booking:
            return jsonify({
                "message": "Booking not found."
            }), 404

        # User can cancel only their own booking
        if booking.user_id != user.id:
            return jsonify({
                "message": "Access denied."
            }), 403

        # Already cancelled?
        if booking.status == "Cancelled":
            return jsonify({
                "message": "Booking is already cancelled."
            }), 400

        # Cancel booking
        booking.status = "Cancelled"

        # Increase available slots
        booking.trek.available_slots += 1

        db.session.commit()

        return jsonify({
            "message": "Booking cancelled successfully."
        }), 200


    @app.route("/admin/bookings", methods=["GET"])
    @jwt_required()
    def admin_bookings():

        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        bookings = Booking.query.all()

        booking_list = []

        for booking in bookings:

            booking_list.append({
                "booking_id": booking.id,
                "user_name": booking.user.name,
                "user_email": booking.user.email,
                "trek_name": booking.trek.name,
                "staff_name": booking.trek.staff.name if booking.trek.staff else None,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": booking.status,
                "payment_status": booking.payment_status
            })

        return jsonify(booking_list), 200






    return app

    

