from fastapi import FastAPI
from debug_toolbar.middleware import DebugToolbarMiddleware
from sqladmin import Admin
from src.database import engine
from src.admin import UserAdmin, NotificationAdmin, authentication_backend


app = FastAPI(debug=True)
app.add_middleware(DebugToolbarMiddleware, panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"])
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(NotificationAdmin)
