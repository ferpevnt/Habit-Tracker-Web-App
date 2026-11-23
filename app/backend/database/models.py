from database.database import Base
from sqlalchemy import Column, Integer, SmallInteger, String, TIMESTAMP, text, ForeignKey, Boolean, Date, UniqueConstraint
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False)
    timezone = Column(String, nullable=False, default="UTC")
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"))
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=text("now()"))

    habits = relationship(
        "Habit",
        back_populates="user",
        cascade="all, delete-orphan")
    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True)
    name = Column(String(50), nullable=False)
    emoji = Column(String(10), nullable=True)
    color = Column(String(50), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"))

    user = relationship("User", back_populates="categories")
    habits = relationship("Habit", back_populates="category")

    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_category"),)

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    emoji = Column(String(10), nullable=True)
    color = Column(String(50), nullable=False, default="#8b5cf6")
    target_frequency = Column(SmallInteger, nullable=False, default=7)
    reminder_time = Column(String(5), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"))
    archived_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="habits")
    category = relationship("Category", back_populates="habits")
    completions = relationship(
        "HabitCompletion",
        back_populates="habit",
        cascade="all, delete-orphan")

class HabitCompletion(Base):
    __tablename__ = "habit_status_days"

    id = Column(Integer, primary_key=True)
    habit_id = Column(
        Integer,
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True)
    completed_date = Column(Date, nullable=False)
    note = Column(String(500), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"))

    habit = relationship("Habit", back_populates="completions")