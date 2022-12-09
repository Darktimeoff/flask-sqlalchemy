from database import db
import enum
from sqlalchemy import Column, Integer, String, Enum, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Role(enum.Enum):
    customer = 1
    executor = 2


class User(db.Model):  # type: ignore
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))
    role = Column(Enum(Role))
    phone = Column(String)

    orders_customer = relationship('Order', foreign_keys='Order.customer_id')
    orders_executor = relationship("Order", foreign_keys="Order.executor_id")
    offers = relationship("Offer", back_populates='user')

    @property
    def serialized(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role.name,
            "phone": self.phone,
        }

    def __repr__(self) -> str:
        return f'<User id:{self.id} name:{self.first_name} {self.last_name} />'


class Offer(db.Model):  # type: ignore
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)

    executor_id = Column(Integer, ForeignKey('users.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    user = relationship('User', back_populates='offers')
    order = relationship('Order', back_populates='offers')

    @property
    def serialized(self):
        return {
            "id": self.id,
            "executor_id": self.executor_id,
            "order_id": self.order_id,
        }

    def __repr__(self):
        return f'<Offer id:{self.id} user_id:{self.executor_id} />'


class Order(db.Model):  # type: ignore
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(250))
    start_date = Column(Date)
    end_date = Column(Date)
    address = Column(String(100))
    price = Column(DECIMAL)

    customer_id = Column(Integer, ForeignKey('users.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))

    user_customer = relationship(
        User, foreign_keys=customer_id,  overlaps="orders_customer")
    user_executor = relationship(
        User, foreign_keys=executor_id,  overlaps="orders_executor")

    offers = relationship(Offer, back_populates='order')

    @property
    def serialized(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price
        }

    def __repr__(self):
        return f'<Order id:{self.id} name:{self.name} address:{self.address} />'
