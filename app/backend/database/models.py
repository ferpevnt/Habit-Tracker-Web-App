from database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship


# ===== EXAMPLE MODEL (delete me) =====
class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )


# ===== YOUR MODELS =====
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False, unique=True)
#     hashed_password = Column(String, nullable=False)
#     created_date = Column(
#         TIMESTAMP(timezone=True),
#         nullable=False,
#         server_default=text("now()"),
#     )
