import sqlalchemy as sa
import random
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def create_password(length = 16):
    password = ''
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(length):
        password+= random.choice(chars)

    return password


email_link = sa.Table("registration_link", Base.metadata,
    sa.Column('email_id', sa.Integer, sa.ForeignKey('reg_form.id')),
    sa.Column('link_id', sa.Integer, sa.ForeignKey('recovery_password.id')),
    )


class Registration(Base):
    __tablename__ = 'reg_form'
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(256), nullable = False)
    surname = sa.Column(sa.String(256), nullable = False)
    email = sa.Column(sa.String(256), nullable = False, unique = True)
    default_password = sa.Column(sa.String(16), nullable = False)
    changed_password = sa.Column(sa.String(16), nullable = True)
    password_is_changed = sa.Column(sa.Boolean, nullable = False, default = False)
    is_paid = sa.Column(sa.Boolean, nullable = False, default = False)
    name_added = sa.Column(sa.String(256), nullable = True)
    surname_added = sa.Column(sa.String(256), nullable = True)
    recoveries = relationship('Recovery', secondary = email_link, back_populates = 'registrations')

class Recovery(Base):
    __tablename__ = 'recovery_password'
    id = sa.Column(sa.Integer, primary_key = True)
    registrations = relationship('Registration', secondary = email_link, back_populates = 'recoveries')
    link_id = sa.Column(sa.String(30), nullable = False, unique = True)

class Role:
    def __init__(self):
        self.engine = sa.create_engine("sqlite:///database2.sqlite")
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        Base.metadata.create_all(self.engine)

class User(Role):

    def register(self, name, surname, email):
        default_password = create_password()
        user = self.session.query(Registration).filter(Registration.email == email).scalar()
        if user == None:
            reg = Registration(name = name, surname = surname, email = email, default_password = default_password)
            self.session.add(reg)
            self.session.commit()
            return default_password
        else:
            self.session.commit()
            return None

    def signin(self, email, password):
        password_check = self.session.query(Registration.password_is_changed).filter(Registration.email == email).scalar()
        if password_check == True:
            exists = self.session.query(Registration).filter(Registration.email == email, Registration.changed_password == password).scalar()
        else:
            exists = self.session.query(Registration).filter(Registration.email == email, Registration.default_password == password).scalar()
        if exists != None:
            return exists.id

    def recover_password(self, email):
        registration = self.session.query(Registration).filter(Registration.email == email).scalar()
        if registration != None:
            link_id = str(create_password(length = 20))
            link = 'http://127.0.0.1:5000/recover/'+link_id
            recovery = Recovery(link_id = link_id)
            recovery.registrations.append(registration)
            self.session.add(recovery)
            self.session.commit()
            return link
        else:
            return None
           

    #def change_data(self, name, email, password):
        #user = session.query(Registration).filter_by(email = email).first()
        #user.changed_password = password
        #user.name = name
        #self.session.commit()

