from marshmallow import Schema, fields

from models.history import History

from app import ma


class GetHistorySchema(Schema):  # type: ignore
    point_id = fields.Str(allow_none=False, required=True)
    from_time = fields.Date(allow_none=False, required=True)
    to_time = fields.Date(allow_none=False, required=True)


class CreateHistorySchema(Schema):  # type: ignore
    point_id = fields.Str(allow_none=False, required=True)
    ts = fields.DateTime(allow_none=False, required=True)
    quantity = fields.Str(allow_none=False, required=True)
    unit = fields.Str(allow_none=False, required=True)


class LoginSchema(Schema):  # type: ignore
    email = fields.Email(allow_none=False, required=True)
    password = fields.Str(allow_none=False, required=True)


class HistorySchema(ma.ModelSchema):  # type: ignore
    class Meta:
        model = History
        exclude = ("updated_at", "created_at")


history_schema = HistorySchema(many=True)
login_schema = LoginSchema()
get_history_schema = GetHistorySchema()
post_history_schema = CreateHistorySchema(many=True)
