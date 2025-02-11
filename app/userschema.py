from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import User
from app.reviewschema import ReviewSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ('password',) # we dont want to return the password

    reviews = fields.Nested(ReviewSchema, many=True, exclude=('user',))