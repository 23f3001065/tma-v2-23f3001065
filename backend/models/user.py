from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )

    staff_profile = db.relationship(
        "StaffProfile",
        backref="user",
        uselist=False
    )

    def __repr__(self):
        return f"<User {self.email}>"