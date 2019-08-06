from datetime import datetime

from server import db


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    name = db.Column(db.String(120), index=True, nullable=False)
    surname = db.Column(db.String(120), index=True, nullable=False)
    photo_url = db.Column(db.String(120), index=True, nullable=True)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    last_modified_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        index=True,
        nullable=False,
        default=datetime.utcnow)
    last_modified_at = db.Column(
        db.DateTime,
        index=True,
        nullable=False,
        default=datetime.utcnow)
    is_deleted = db.Column(
        db.Boolean,
        index=True,
        nullable=False,
        default=False)

    def __str__(self):
        template = dict(
            id=self.id,
            email=self.email,
            name=self.name,
            surname=self.surname,
            photo_url=self.photo_url,
            created_by=self.created_by,
            last_modified_by=self.last_modified_by,
            created_at=self.created_at,
            last_modified_at=self.last_modified_at,
            is_deleted=self.is_deleted
        )
        return template
