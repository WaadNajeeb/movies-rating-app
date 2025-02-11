from dataclasses import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.review import Review
from app.models.user import User


class UserReview(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        # we dont need to return columns that we dont need to the frontend
        exclude = ('password', 'firstname', 'lastname', 'id', 'email') 

    profile_picture = fields.Str(allow_none=True) 
    full_name = fields.Str(allow_none=True) 

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        include_fk = True

    user = fields.Nested(UserReview)
    created_at = fields.DateTime(format="%d %B %Y %I:%M %p") 
