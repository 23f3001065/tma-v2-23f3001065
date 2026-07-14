from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    duration_days = db.Column(
        db.Integer,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    available_slots = db.Column(
        db.Integer,
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff_profiles.id")
    )

    bookings = db.relationship(
        "Booking",
        backref="trek",
        lazy=True
    )

    def __repr__(self):
        return f"<Trek {self.name}>"
    

    def to_json(self):

        staff_name = None

        if self.staff_profile:
            if self.staff_profile.user:
                staff_name = self.staff_profile.user.name

        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "difficulty": self.difficulty,
            "duration_days": self.duration_days,
            "description": self.description,
            "available_slots": self.available_slots,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "status": self.status,
            "staff_id": self.staff_id,
            "staff_name": staff_name,
            "participant_count": len([
                booking
                for booking in self.bookings
                if booking.status == "Booked"
            ])
        }