from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from sqlalchemy.future import select
from secrets import token_hex
from src.models import User, Notification
from src.database import async_session_maker
from src.tasks import send_messages
from src.config import TOKEN, ADMIN_LOGIN, ADMIN_PASSWORD


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
    column_searchable_list = [User.username]


class NotificationAdmin(ModelView, model=Notification):
    column_list = [Notification.id, Notification.text]

    async def after_model_change(self, data, model, is_created, request):
        if is_created:
            session = async_session_maker()
            result = await session.execute(select(User.chat_id).filter(User.id.in_(map(lambda x: int(x), data['users']))))
            users = result.scalars().all()
            send_messages.apply_async((data['text'], users), eta=data['datetime'])


class AdminAuth(AuthenticationBackend):
    tokens = []

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            token = token_hex(10)
            request.session.update({"token": token})
            self.tokens.append(token)
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if token in self.tokens:
            return True
        else:
            return False


authentication_backend = AdminAuth(secret_key=TOKEN)
