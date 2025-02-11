from dataclasses import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ('password',) # we dont want to return the password

    reviews = fields.Nested('ReviewSchema', many=True, exclude=('user',)) #Linking reviews
    profile_picture = fields.Str(allow_none=True) #property
    full_name = fields.Str(allow_none=True)  #property