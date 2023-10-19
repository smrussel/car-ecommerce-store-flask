import jwt
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# timestamp to be inherited by other class models
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


@login.user_loader  # new code entry
def load_user(id):  # new code entry
    return User.query.get(int(id))
    # new code entry --- # slightly modified such that the user is loaded based on the id in the db


# user class
class User(db.Model, TimestampMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Integer, default=0)
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    cars = db.relationship('Car', backref='user', lazy='dynamic')

    # print to console username created
    def __repr__(self):
        return f'<User {self.username}>'

    # generate user password i.e. hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check user password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # for reseting a user password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    # verify token generated for resetting password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Car(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    car_title = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    reg_no = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    gearbox = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    car_photo = db.Column(db.String(255), nullable=False, default='default.jpg')
    car_photo_1 = db.Column(db.String(255), nullable=False, default='default.jpg')
    car_photo_2 = db.Column(db.String(255), nullable=False, default='default.jpg')
    car_photo_3 = db.Column(db.String(255), nullable=False, default='default.jpg')
    car_photo_4 = db.Column(db.String(255), nullable=False, default='default.jpg')
    miles = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(255), nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    available = db.Column(db.Integer, default=True, nullable=False)
    reviews = db.relationship('Review', backref='car', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Car {self.car_title}>'


class Blog(db.Model, TimestampMixin):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Blog {self.title}>'


class Review(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))


class ReserveModel(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    duration_day = db.Column(db.Integer, nullable=False, default=7)

    def __repr__(self):
        return '<ReserveModel %r>' % self.reference_number


class CarReserve(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(250), nullable=False)
    reserve_id = db.Column(db.Integer, db.ForeignKey('reserve_model.id'), nullable=False)
    reserve = db.relationship('ReserveModel', backref=db.backref('reserves', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    car = db.relationship('Car', backref=db.backref('reserved_cars', lazy=True))

    def __repr__(self):
        return f'<CarReserve {self.reference_number}>'


class CustomerOrderModel(db.Model,TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<CustomerOrderModel %r>' % self.invoice


# Order related product info saved in this model
class OrderProductModel(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('customer_order_model.id'), nullable=False)
    order = db.relationship('CustomerOrderModel', backref=db.backref('orders', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    car = db.relationship('Car', backref=db.backref('ordered_cars', lazy=True))
    car_title = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    color = db.Column(db.Text, nullable=False)


class FaqModel(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)


class TradeModel(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))