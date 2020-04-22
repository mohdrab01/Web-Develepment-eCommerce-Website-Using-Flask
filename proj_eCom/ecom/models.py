from datetime import datetime
from ecom import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##### DB CLASSES #####
##### USER DB #####
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

##### PRODUCT DB #####
class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    regular_price = db.Column(db.DECIMAL(10,2))
    discounted_price = db.Column(db.DECIMAL(10,2))
    product_rating = db.Column(db.DECIMAL(2,1))
    def __repr__(self):
        return f"Product('{self.productid}','{self.product_name}','{self.description}', '{self.image}',  '{self.quantity}', '{self.regular_price}', '{self.discounted_price}')"

##### CART DB #####
class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Cart('{self.id}', '{self.productid}', '{self.quantity}')"

##### ORDER DB #####
class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    ordered_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f"Order('{self.id}', '{self.productid}', '{self.quantity}' , '{self.ordered_date}')"

##### ROUTES #####

if __name__=='__main__':
    app.run(debug=True)
            