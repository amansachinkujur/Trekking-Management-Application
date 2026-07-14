from celery_worker import celery
from flask_mail import Message
from app import mail, db
from datetime import date, timedelta
from app.models import Booking, Trek, User
from sqlalchemy import func
import csv
import os

@celery.task
def send_daily_reminders():

    tomorrow = date.today() + timedelta(days=1)

    print(f"Today: {date.today()}")
    print(f"Tomorrow: {tomorrow}")

    bookings = Booking.query.filter_by(status="Booked").all()

    print(f"Total booked bookings: {len(bookings)}")

    for booking in bookings:

        trek = booking.trek

        print("--------------------------")
        print(f"Booking ID: {booking.id}")
        print(f"User: {booking.user.email}")
        print(f"Trek: {trek.name}")
        print(f"Trek Start Date: {trek.start_date}")

        if trek.start_date != tomorrow:
            print("Skipped")
            continue

        print("Sending email...")

        msg = Message(
            subject="Trek Reminder",
            sender=mail.default_sender,
            recipients=[booking.user.email]
        )

        msg.body = f"""
Hello {booking.user.name},

This is a reminder that your trek "{trek.name}" starts tomorrow ({trek.start_date}).

Please arrive on time and carry all necessary trekking equipment.

Happy Trekking!
"""

        mail.send(msg)

        print(f"Email sent to {booking.user.email}")

    return "Daily reminders sent."



@celery.task
def send_monthly_report():

    total_treks = Trek.query.filter_by(status="Completed").count()

    participants = db.session.query(Booking.user_id).distinct().count()

    total_bookings = Booking.query.count()

    popular = (
        db.session.query(
            Trek.name,
            func.count(Booking.id).label("count")
        )
        .join(Booking)
        .group_by(Trek.id)
        .order_by(func.count(Booking.id).desc())
        .first()
    )

    if popular:
        popular_trek = popular.name
        popular_count = popular.count
    else:
        popular_trek = "N/A"
        popular_count = 0

    admin = User.query.filter_by(role="admin").first()



    msg = Message(
        subject=f"Monthly Trekking Activity Report {date.today().strftime('%Y-%m')}",
        sender=mail.default_sender,
        recipients=[admin.email]
    )

    msg.html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">

        <h2>Monthly Trekking Activity Report {date.today().strftime('%Y-%m')}</h2>

        <table border="1" cellpadding="8" cellspacing="0">

            <tr>
                <th align="left">Metric</th>
                <th align="left">Value</th>
            </tr>

            <tr>
                <td>Total Treks Conducted</td>
                <td>{total_treks}</td>
            </tr>

            <tr>
                <td>Total Registered Users</td>
                <td>{participants}</td>
            </tr>

            <tr>
                <td>Total Bookings</td>
                <td>{total_bookings}</td>
            </tr>

            <tr>
                <td>Most Popular Trek</td>
                <td>{popular_trek}</td>
            </tr>

            <tr>
                <td>Bookings for Popular Trek</td>
                <td>{popular_count}</td>
            </tr>

        </table>

        <br>

        <p>
            This report was generated automatically by the
            <b>Trekking Management Application</b>.
        </p>

    </body>
    </html>
    """

    mail.send(msg)

    print("Monthly report emailed successfully.")

    return "Monthly report sent."


#Exporting booking hsitory to CSV (User requested)
@celery.task
def export_booking_history(user_id):

    user = User.query.get(user_id)

    bookings = Booking.query.filter_by(user_id=user_id).all()

    filename = f"booking_history_{user_id}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([

            "User ID",

            "Trek Name",

            "Location",

            "Booking Status",

            "Booking Date"

        ])

        for booking in bookings:

            writer.writerow([

                booking.user_id,

                booking.trek.name,

                booking.trek.location,

                booking.status,

                booking.booking_date

            ])

    msg = Message(

        subject="Your Booking History CSV",

        sender=mail.default_sender,

        recipients=[user.email]

    )

    msg.body = "Your booking history CSV is attached."

    with open(filename, "rb") as f:

        msg.attach(

            filename,

            "text/csv",

            f.read()

        )

    mail.send(msg)

    os.remove(filename)

    return "CSV Export Completed"