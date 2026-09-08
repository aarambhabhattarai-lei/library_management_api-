from sqlalchemy import Column, Integer, String, Boolean , DateTime
import sqlalchemy
from sqlalchemy.sql.expression import func, null
from database import Base 
from datetime import datetime

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    published_year = Column(Integer, nullable=True)
    available = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    join_date = Column(DateTime, nullable=True ,server_default=func.now())

class BorrowedBooks(Base):
    __tablename__ = "borrowed_books"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    book_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    borrowed_date = Column(DateTime,server_default=func.now(), nullable=True)
    returned_date = Column(DateTime, nullable=True)