from sqlalchemy import Column, Integer, String

from .db import Base


class JokeTable(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    joke = Column(String, index=True)
