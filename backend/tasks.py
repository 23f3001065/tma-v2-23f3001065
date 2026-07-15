import os
import sys
import csv

from io import StringIO

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from celery_app import celery
from flask_mail import Message
from extensions import mail
from models.user import User
from models.booking import Booking

@celery.task
def send_test_email():

    from app_factory import create_app
    app = create_app()
    with app.app_context():

        msg = Message(
            subject="Trekking Management Application",
            recipients=[os.getenv("MAIL_USER")],
            body='''Trekking Management Application: 

            Test email sent using Celery. 
            
            Regards,
            Bhavana Gupta
            '''
        )

        mail.send(msg)

        print("Email sent successfully.")

@celery.task
def export_booking_history(user_id):

    from app_factory import create_app
    app = create_app()
    with app.app_context():

        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        
        bookings = Booking.query.filter_by(user_id=user.id).all()

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "User ID",
            "Trek Name",
            "Location",
            "Booking Date",
            "Status"
        ])

        for booking in bookings:

            writer.writerow([
                booking.user.id,
                booking.trek.name,
                booking.trek.location,
                booking.booking_date,
                booking.status
            ])

        csv_data = output.getvalue()

        msg = Message(
            subject="Your Trek Booking History",
            recipients=[user.email]
        )

        msg.body = ("Please find your booking history attached.")

        msg.attach(
            "booking_history.csv",
            "text/csv",
            csv_data)

        mail.send(msg)

        print("Booking history emailed.")

from datetime import date

@celery.task
def send_daily_reminders():

    from app_factory import create_app

    app = create_app()

    with app.app_context():

        today = date.today()

        bookings = Booking.query.filter_by(
            status="Booked"
        ).all()

        for booking in bookings:

            if booking.trek.start_date == today:

                msg = Message(

                    subject="Trek Reminder",

                    recipients=[booking.user.email],

                    body=f"""
Hello {booking.user.name},

Reminder for your trek:

Trek: {booking.trek.name}
Location: {booking.trek.location}
Start Date: {booking.trek.start_date}

Please arrive on time.

Regards,
Trekking Management Application
"""
                )

                mail.send(msg)

        print("Daily reminders sent.")

@celery.task
def send_monthly_admin_report():

    from app_factory import create_app

    app = create_app()

    with app.app_context():

        total_treks = Booking.query.count()

        total_participants = Booking.query.filter_by(
            status="Booked"
        ).count()

        msg = Message(

            subject="Monthly Trekking Report",

            recipients=["admin@gmail.com"]
        )

        msg.html = f"""
<h2>Monthly Trekking Report</h2>

<p>Total Bookings: {total_treks}</p>

<p>Total Participants: {total_participants}</p>
"""

        mail.send(msg)

        print("Monthly report sent.")