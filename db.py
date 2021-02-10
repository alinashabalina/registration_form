import sqlalchemy as sa
import random
from sqlalchemy import Column, Integer, Datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def create_password():
    length = 16;
    password = '';
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(length):
        password+= random.choice(chars)

    return password

class Registration(Base):
    __tablename__ = 'reg_form'
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(256), nullable = False)
    email = sa.Column(sa.String(256), nullable = False, unique = True)
    default_password = sa.Column(sa.String(16), nullable = False)
    changed_password = sa.Column(sa.String(16), nullable = True)
    
class Role:
    def __init__(self):
        self.engine = sa.create_engine("sqlite:///database2.sqlite")
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        Base.metadata.create_all(self.engine)

class User(Role):

    def register(self, name, email):
        user = Registration(name = name, email = email, default_password = create_password())
        self.session.add(user)
        self.session.commit()

    def change_data(self, name, email, password):
        user = session.query(Registration).filter_by(email = email).first()
        user.changed_password = password
        user.name = name
        self.session.commit()


    
