from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner = db.relationship("User", back_populates="images")
    review = db.relationship("Review", back_populates = "images")
    business = db.relationship("Business", back_populates = "images")

    def to_dict(self):
        return {
            "id" : self.id,
            "url" : self.url,
            "stars" : self.stars,
            "owner_id" : self.owner_id,
            "business_id" : self.business_id,
            "review_id" : self.review_id,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
        }