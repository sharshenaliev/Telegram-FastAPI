from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import MetaData, Column, Integer, String, Text, DateTime, ForeignKey, Table


metadata = MetaData()

Base = declarative_base(metadata=metadata)


user_notification_association = Table(
    'user_notification',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('notification_id', Integer, ForeignKey('notification.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)

    notifications = relationship(
        "Notification",
        secondary=user_notification_association,
        back_populates="users"
    )

    def __repr__(self):
        return self.username


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)

    users = relationship(
        "User",
        secondary=user_notification_association,
        back_populates="notifications"
    )

    def __repr__(self):
        return str(self.id)
