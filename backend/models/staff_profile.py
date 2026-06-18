from extensions import db


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    contact_no = db.Column(
        db.String(15)
    )

    experience_years = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="active"
    )

    treks = db.relationship(
        "Trek",
        backref="staff_profile",
        lazy=True
    )

    def __repr__(self):
        return f"<StaffProfile {self.id}>"