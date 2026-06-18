from extensions import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="Booked"
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "trek_id",
            name="unique_user_trek_booking"
        ),
    )

    def __repr__(self):
        return f"<Booking {self.id}>"