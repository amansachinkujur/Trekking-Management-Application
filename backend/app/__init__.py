from flask import Flask, app,request, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime
from flask_mail import Mail
from flask_caching import Cache
from flask_mail import Message





db = SQLAlchemy()

jwt = JWTManager()
mail = Mail()
cache = Cache()
from app.models import User, Trek, Booking, StaffProfile
from app import cache

def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    jwt.init_app(app)
    mail.init_app(app)
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    cache.init_app(app)
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

    #Booking export route (user)
    
    @app.route("/bookings/export", methods=["POST"])
    @jwt_required()
    def export_csv():
        from app.tasks import export_booking_history
        user_id = int(get_jwt_identity())

        export_booking_history.delay(user_id)

        return jsonify({

            "message":
            "CSV export started. It will be emailed shortly."

        })






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
        #clear redis cache for treks list
        cache.clear()

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
        #clear redis cache for treks list
        cache.clear()
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
        #clear redis cache for treks list
        cache.clear()
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
        is_active = data.get("is_active", True)
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
            is_active=is_active
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


    #Users list for admin
    @app.route("/admin/users", methods=["GET"])
    @jwt_required()
    def get_users():

        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        users = User.query.filter_by(role="user").all()

        user_list = []

        for user in users:

            user_list.append({

                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "is_active": user.is_active

            })

        return jsonify(user_list), 200

# Edit User (Admin)

    @app.route("/admin/users/<int:user_id>", methods=["PUT"])
    @jwt_required()
    def update_user(user_id):

        # Check logged-in user
        admin_id = int(get_jwt_identity())
        admin = db.session.get(User, admin_id)

        if admin.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find user
        user = db.session.get(User, user_id)

        if not user or user.role != "user":
            return jsonify({
                "message": "User not found."
            }), 404

        data = request.get_json()

        # Update name
        if data.get("name"):
            user.name = data.get("name")

        # Update email
        if data.get("email"):

            existing = User.query.filter(
                User.email == data.get("email"),
                User.id != user.id
            ).first()

            if existing:
                return jsonify({
                    "message": "Email already exists."
                }), 409

            user.email = data.get("email")

        # Update phone
        if data.get("phone"):
            user.phone = data.get("phone")

        # Update password (optional)
        if data.get("password"):
            user.set_password(data.get("password"))

        # Activate / Deactivate
        if "is_active" in data:
            user.is_active = data.get("is_active")

        db.session.commit()

        return jsonify({
            "message": "User updated successfully."
        }), 200




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

    #Staff Update Route
    @app.route("/staff/<int:staff_id>", methods=["PUT"])
    @jwt_required()
    def update_staff(staff_id):

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find staff
        staff = db.session.get(User, staff_id)

        if not staff or staff.role != "staff":
            return jsonify({
                "message": "Staff not found."
            }), 404

        data = request.get_json()

        if data.get("name"):
            staff.name = data.get("name")

        if data.get("email"):

            existing = User.query.filter(
                User.email == data.get("email"),
                User.id != staff.id
            ).first()

            if existing:
                return jsonify({
                    "message": "Email already exists."
                }), 409

            staff.email = data.get("email")

        if data.get("phone"):
            staff.phone = data.get("phone")

        if data.get("password"):
            staff.set_password(data.get("password"))

        if "is_active" in data:
            staff.is_active = data.get("is_active")

        db.session.commit()

        return jsonify({
            "message": "Staff updated successfully."
        }), 200

    #Staff Delete Route
    @app.route("/staff/<int:staff_id>", methods=["DELETE"])
    @jwt_required()
    def delete_staff(staff_id):

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        # Find staff
        staff = db.session.get(User, staff_id)

        if not staff or staff.role != "staff":
            return jsonify({
                "message": "Staff not found."
            }), 404

        assigned_trek = Trek.query.filter_by(
            assigned_staff_id=staff.id
        ).first()

        if assigned_trek:
            return jsonify({
                "message": "Cannot delete staff assigned to a trek."
            }), 400

        db.session.delete(staff)
        db.session.commit()

        return jsonify({
            "message": "Staff deleted successfully."
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

#user treks api

    @app.route("/user/treks", methods=["GET"])
    @cache.cached()
    @jwt_required()
    def get_user_treks():
        #test if cache data is shown or direct query from db
        #print("Fetching treks from database...")
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        if user.role != "user":
            return jsonify({
                "message": "Access denied."
            }), 403

        treks = Trek.query.filter(
            Trek.status.in_(["Approved", "Open"])
        ).all()

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

#User updating their profile
    @app.route("/profile", methods=["PUT"])
    @jwt_required()
    def update_profile():

        # Logged-in user
        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        data = request.get_json()

        # Update name
        if data.get("name"):
            user.name = data.get("name")

        # Update email
        if data.get("email"):

            existing = User.query.filter(
                User.email == data.get("email"),
                User.id != user.id
            ).first()

            if existing:
                return jsonify({
                    "message": "Email already exists."
                }), 409

            user.email = data.get("email")

        # Update phone
        if data.get("phone"):
            user.phone = data.get("phone")

        # Update password
        if data.get("password"):
            user.set_password(data.get("password"))

        db.session.commit()

        return jsonify({
            "message": "Profile updated successfully."
        }), 200

    #Staff assigned treks route
    @app.route("/staff/treks", methods=["GET"])
    @jwt_required()
    def get_staff_treks():

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user or user.role != "staff":
            return jsonify({
                "message": "Access denied."
            }), 403

        treks = Trek.query.filter_by(
            assigned_staff_id=user.id
        ).all()
        



        trek_list = []

        for trek in treks:

            trek_list.append({

                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "available_slots": trek.available_slots,
                "status": trek.status,
                "start_date": trek.start_date.strftime("%Y-%m-%d"),
                "registered_users": Booking.query.filter_by(
                                    trek_id=trek.id,
                                    status="Booked"
                                    ).count(),

            })

        return jsonify(trek_list), 200

    #Staff Update assigned trek
    @app.route("/staff/treks/<int:trek_id>", methods=["PUT"])
    @jwt_required()
    def update_staff_trek(trek_id):

        # Check logged-in staff
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user or user.role != "staff":
            return jsonify({
                "message": "Access denied."
            }), 403

        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        # Staff can update only their own trek
        if trek.assigned_staff_id != user.id:
            return jsonify({
                "message": "You are not assigned to this trek."
            }), 403

        data = request.get_json()

        if data.get("available_slots") is not None:
            trek.available_slots = data.get("available_slots")

        if data.get("status"):

            if data.get("status") not in [
                "Open",
                "Closed",
                "Completed"
            ]:

                return jsonify({
                    "message": "Invalid trek status."
                }), 400

            trek.status = data.get("status")

        db.session.commit()

        return jsonify({
            "message": "Trek updated successfully."
        }), 200

    #View Trek participants (Staff)
    @app.route("/staff/treks/<int:trek_id>/bookings", methods=["GET"])
    @jwt_required()
    def get_staff_trek_bookings(trek_id):

        # Check logged-in staff
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user or user.role != "staff":
            return jsonify({
                "message": "Access denied."
            }), 403

        trek = db.session.get(Trek, trek_id)

        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        # Staff can view only their own trek participants
        if trek.assigned_staff_id != user.id:
            return jsonify({
                "message": "You are not assigned to this trek."
            }), 403

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        booking_list = []

        for booking in bookings:

            booking_list.append({

                "booking_id": booking.id,
                "user_name": booking.user.name,
                "user_email": booking.user.email,
                "user_phone": booking.user.phone,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": booking.status,
                "payment_status": booking.payment_status

            })

        return jsonify(booking_list), 200


    #Admin Stats api(dashboard)
    @app.route("/admin/statistics", methods=["GET"])
    @jwt_required()
    def admin_statistics():

        # Check logged-in user
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user or user.role != "admin":
            return jsonify({
                "message": "Access denied."
            }), 403

        total_treks = Trek.query.count()

        total_users = User.query.filter_by(
            role="user"
        ).count()

        total_staff = User.query.filter_by(
            role="staff"
        ).count()

        total_bookings = Booking.query.count()

        open_treks = Trek.query.filter_by(
            status="Open"
        ).count()

        completed_treks = Trek.query.filter_by(
            status="Completed"
        ).count()

        cancelled_bookings = Booking.query.filter_by(
            status="Cancelled"
        ).count()

        popular_trek = db.session.query(
            Trek.name,
            db.func.count(Booking.id).label("total")
        ).join(
            Booking,
            Booking.trek_id == Trek.id
        ).group_by(
            Trek.id
        ).order_by(
            db.func.count(Booking.id).desc()
        ).first()

        return jsonify({

            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,

            "open_treks": open_treks,
            "completed_treks": completed_treks,
            "cancelled_bookings": cancelled_bookings,

            "popular_trek":
                popular_trek.name if popular_trek else "None"

        }), 200






    return app

    

