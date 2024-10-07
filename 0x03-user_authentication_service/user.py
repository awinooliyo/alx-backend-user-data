#!/usr/bin/env python3
""" User Module """


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return (f"<User(id={self.id}, email='{self.email}', "
                f"session_id='{self.session_id}', "
                f"reset_token='{self.reset_token}')>")


engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(email='example@example.com',
                hashed_password='hashed_password_example')
session.add(new_user)
session.commit()
