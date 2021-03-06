import sqlalchemy as sa
import random
from datetime import datetime
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


def create_password(length=16):
    password = ''
    chars = '-=_abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(length):
        password += random.choice(chars)

    return password




email_link = sa.Table('registration_link', Base.metadata,
                      sa.Column('email_id', sa.Integer,
                                sa.ForeignKey('reg_form.id')),
                      sa.Column('link_id', sa.Integer,
                                sa.ForeignKey('recovery_password.id')),
                      )

info = sa.Table('info', Base.metadata, sa.Column('user_id', sa.Integer,sa.ForeignKey('reg_form.id')),
sa.Column('user_info', sa.Integer, sa.ForeignKey('user_info.id'))
)

class Registration(Base):
    __tablename__ = 'reg_form'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    surname = sa.Column(sa.String(100), nullable=False)
    email = sa.Column(sa.String(100), nullable=False, unique=True)
    default_password = sa.Column(sa.String(16), nullable=False)
    changed_password = sa.Column(sa.String(16), nullable=True)
    password_is_changed = sa.Column(sa.Boolean, nullable=False, default=False)
    is_paid = sa.Column(sa.Boolean, nullable=False, default=False)
    name_added = sa.Column(sa.String(100), nullable=True)
    surname_added = sa.Column(sa.String(100), nullable=True)

    recoveries = relationship(
        'Recovery', secondary=email_link, back_populates='registrations')



class Recovery(Base):
    __tablename__ = 'recovery_password'
    id = sa.Column(sa.Integer, primary_key=True)
    link_id = sa.Column(sa.String(30), nullable=False, unique=True)

    registrations = relationship(
        'Registration', secondary=email_link, back_populates='recoveries')


class User_info(Base):
    __tablename__ = 'user_info'
    id = sa.Column(sa.Integer, primary_key = True)
    likes = sa.Column(sa.Integer, nullable=False)
    payments = sa.Column(sa.Integer, nullable = False, default = 0)
    user_id = sa.Column(sa.Integer, nullable = False)
    liked_photos = sa.Column(sa.Integer, nullable = False, default = 0)
    photos_uploaded = sa.Column(sa.Integer, nullable = False, default = 0)
    last_updated = sa.Column(sa.DateTime, nullable = False)
    

class Photo_info(Base):
    __tablename__ = 'photo_info'
    id = sa.Column(sa.Integer, primary_key = True)
    user_id = sa.Column(sa.Integer, nullable = False)
    name = sa.Column(sa.String, nullable = False)
    description = sa.Column(sa.String(150), nullable = False)
    total_likes = sa.Column(sa.Integer, nullable = False, default = 0)


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
        user = self.session.query(Registration).filter(
            Registration.email == email).scalar()
        if user == None:
            reg = Registration(name=name, surname=surname,
                               email=email, default_password=default_password)
            self.session.add(reg)
            self.session.commit()
            user_info = User_info(likes = 5, user_id = reg.id, last_updated = datetime.now())
            self.session.add(user_info)
            self.session.commit()
            return default_password
        else:
            self.session.commit()
            return None

    def signin(self, email, password):
        password_check = self.session.query(Registration.password_is_changed).filter(
            Registration.email == email).scalar()
        if password_check == True:
            exists = self.session.query(Registration).filter(
                Registration.email == email, Registration.changed_password == password).scalar()
        else:
            exists = self.session.query(Registration).filter(
                Registration.email == email, Registration.default_password == password).scalar()
        if exists != None:
            return exists.id

    def recover_password(self, email):
        registration = self.session.query(Registration).filter(
            Registration.email == email).scalar()
        if registration != None:
            link_id = str(create_password(length=20))
            link = 'http://127.0.0.1:5000/recover/'+link_id
            recovery = Recovery(link_id=link_id)
            recovery.registrations.append(registration)
            self.session.add(recovery)
            self.session.commit()
            return link
        else:
            return None

    def generate_password(self, link_id):
        recovery = self.session.query(Recovery).filter(
            Recovery.link_id == link_id).scalar()
        if recovery != None:
            default_password = create_password()
            recovery.registrations[0].default_password = default_password
            self.session.delete(recovery)
            self.session.commit()
            return default_password
        else:
            return None


    def likes_purchase(self, user_id, number):
        payment_for_one_like = 10
        payment = int(number)*payment_for_one_like
        purchase = self.session.query(User_info).filter(User_info.user_id == user_id).scalar()
        if purchase != None:
            payment_updated = int(purchase.payments) + payment
            likes_updated = int(purchase.likes) + int(number)
            purchase.likes = likes_updated
            purchase.payments = payment_updated
            self.session.commit()
            return purchase
        else:
            purchase = User_info(likes = number, payments = payment, user_id = user_id)
            self.session.add(purchase)
            self.session.commit()
            return purchase
            

    def get_user_info(self, user_id):
        user_info = self.session.query(User_info).filter(User_info.user_id == user_id).scalar()
        if user_info != None:
            return user_info
        else:
            return None

    
    def like_a_photo(self, user_id, photo_id):
        user_info = self.session.query(User_info).filter(User_info.user_id == user_id).scalar()
        photo = self.session.query(Photo_info).filter(Photo_info.id == photo_id).scalar()
        if user_info != None and photo != None:
            liked_photos_updated = int(user_info.liked_photos)+1
            user_info.liked_photos = liked_photos_updated
            total_likes_updated = int(photo.total_likes)+1
            photo.total_likes = total_likes_updated
            self.session.commit()
            response = {'user_info': user_info, 'photo': photo}
            return response
        else:
            return None


    def upload_photos(self, user_id, description, name):
        user = self.session.query(User_info).filter(User_info.user_id == user_id).scalar()
        if user != None:
            photo = Photo_info(user_id = user_id, name = name, description = description)
            photos_uploaded_updated = int(user.photos_uploaded)+1
            user.photos_uploaded = photos_uploaded_updated
            self.session.add(photo)
            self.session.commit()
            return photo
        else:
            return None
        


class System(Role):

    def likes_updated(self):
        needs_updating = self.session.query(User_info).filter(User_info.last_updated <= datetime.now() - datetime.timedelta(days = 1))
        if needs_updating != None:
            for everyone in needs_updating:
                if everyone.likes < 5:
                    everyone.likes = 5
                else: 
                    pass
                everyone.last_updated = datetime.now()
                self.session.commit()
                
        

    def render_photos(self):
        photos = self.session.query(Photo_info).all()
        chosen = []
        for i in range (6):
            a = random.choice(photos)
            chosen.append({'name': a.name,
            'description':a.description,
            'likes':a.total_likes
            })
        return chosen
    
        

