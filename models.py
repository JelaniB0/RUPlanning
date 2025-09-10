from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

class Class(Base):
    __tablename__ = "classes"
    class_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String)
    day_of_week = Column(String)   # e.g. Mon, Tue
    start_time = Column(Time)
    end_time = Column(Time)

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    description = Column(String)
    duration_est = Column(Integer)  # in minutes
    deadline = Column(Date)
    priority = Column(Integer, default=1)

class Commitment(Base):
    __tablename__ = "commitments"
    commitment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    day_of_week = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)