from datetime import date, datetime
from app import app, db
from models.user import User
from models.history import History
from models.building import Building
from models.device import Device

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt


def date_12h_format(view: ModelView, value: datetime) -> str:
    return value.strftime("%m.%d.%Y %I:%M %p")


DATE_12H_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
DATE_12H_FORMATTERS[date] = date_12h_format


class UserModelView(ModelView):  # type: ignore
    column_type_formatters = DATE_12H_FORMATTERS

    column_searchable_list = ["email"]
    page_size = 50
    can_export = True
    column_exclude_list = ["password", "updated_at", "confirmed_at", "user_role"]
    form_excluded_columns = ["password", "updated_at", "confirmed_at", "created_at"]


class CustomModelView(ModelView):  # type: ignore
    column_type_formatters = DATE_12H_FORMATTERS
    page_size = 50
    column_exclude_list = ["created_at", "updated_at"]
    form_excluded_columns = ["created_at", "updated_at"]


# admin
admin = Admin(app, name="Device17 Admin", template_mode="bootstrap3")
admin.add_view(UserModelView(User, db.session))
admin.add_view(CustomModelView(History, db.session))
admin.add_view(CustomModelView(Building, db.session))
admin.add_view(CustomModelView(Device, db.session))
