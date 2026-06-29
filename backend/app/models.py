# Creating models

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)
    # admin | staff | user

    phone = db.Column(db.String(15))

    is_active = db.Column(db.Boolean, default=True)

    # One User -> Many Bookings
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)

    duration = db.Column(db.Integer, nullable=False)  # in days

    available_slots = db.Column(db.Integer, nullable=False)

    # Will be converted to a ForeignKey in the next step
    assigned_staff_id = db.Column(db.Integer)

    status = db.Column(db.String(20), nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    description = db.Column(db.Text)

    # One Trek -> Many Bookings
    bookings = db.relationship("Booking", backref="trek", lazy=True)


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    booking_date = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(20), nullable=False)

    payment_status = db.Column(db.String(20))


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    contact_details = db.Column(db.String(200))

    status = db.Column(db.String(20), nullable=False)