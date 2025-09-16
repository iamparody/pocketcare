import reflex as rx
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    create_engine,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./pocketcare.db"
echo = False
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    profile = relationship("Profile", back_populates="user", uselist=False)
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    distress_logs = relationship("DistressLog", back_populates="user")
    therapist_requests = relationship("TherapistRequest", back_populates="user")
    journals = relationship("Journal", back_populates="user")
    journal_badges = relationship("JournalBadge", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pseudonym = Column(String, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    interests = Column(String)
    bio = Column(Text)
    completed = Column(Boolean, default=False)
    user = relationship("User", back_populates="profile")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(String, default="Basic")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    user = relationship("User", back_populates="subscription")


class PeerChat(Base):
    __tablename__ = "peer_chats"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, unique=True)
    user1_pseudonym = Column(String)
    user2_pseudonym = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("ChatMessage", back_populates="chat")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("peer_chats.id"))
    pseudonym = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    chat = relationship("PeerChat", back_populates="messages")


class PeerQueue(Base):
    __tablename__ = "peer_queue"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pseudonym = Column(String)
    requested_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="waiting")


class DistressLog(Base):
    __tablename__ = "distress_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pseudonym = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(Text)
    severity = Column(String, default="High")
    status = Column(String, default="pending")
    user = relationship("User", back_populates="distress_logs")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    reporter_pseudonym = Column(String)
    reported_pseudonym = Column(String)
    reason = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")


class TherapistRequest(Base):
    __tablename__ = "therapist_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pseudonym = Column(String)
    details = Column(Text)
    urgency = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")
    user = relationship("User", back_populates="therapist_requests")


class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    mood = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="journals")
    is_special = Column(Boolean, default=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class JournalBadge(Base):
    __tablename__ = "journal_badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_name = Column(String)
    awarded_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="journal_badges")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    link = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="notifications")


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=echo
)


@contextmanager
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


def init_db():
    create_db_and_tables()
    with get_db() as db:
        admin = db.query(User).filter(User.username == "admin123").first()
        if not admin:
            admin_user = User(username="admin123", password="admin123", role="admin")
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            admin_profile = Profile(
                user_id=admin_user.id,
                pseudonym="AdminRoot",
                age=99,
                gender="N/A",
                completed=True,
                bio="App Administrator",
            )
            db.add(admin_profile)
            db.commit()