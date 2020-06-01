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
    phno=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

##### PRODUCT DB #####
''' Identify all the products and consider each product as an entity/object.
    Create a DB for each Product.
    All other Gadgets classes must inherit Product class.
    My Gadgets are: Tv,Laptop,Refrigerator,Washing Machine,Mobile '''

class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    regular_price = db.Column(db.DECIMAL(10,2))
    discounted_price = db.Column(db.DECIMAL(10,2))
    product_rating = db.Column(db.DECIMAL(2,1))
    warranty = db.Column(db.String(50), nullable=False)
    catogery = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Product('{self.productid}','{self.product_name}', '{self.image}',  '{self.quantity}', '{self.regular_price}', '{self.discounted_price}', '{self.warranty}', '{self.catogery}')"


#### MOBILE PHONE DB #####
class Mobile(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    ram_size = db.Column(db.Integer, nullable=False)
    int_storage = db.Column(db.Integer, nullable=False)
    ext_storage = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    resolution = db.Column(db.String(100), nullable=False)
    os = db.Column(db.String(100), nullable=False)
    cpu = db.Column(db.String(100), nullable=False)
    camera_front = db.Column(db.DECIMAL(5,2))
    camera_rear = db.Column(db.DECIMAL(5,2))
    battery = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product('{self.productid}','{self.brand}','{self.ram_size}','{self.int_storage}','{self.ext_storage}','{self.color}', '{self.resolution}', '{self.os}', '{self.cpu}', '{self.camera_front}', '{self.camera_rear}', '{self.battery}', )"

##### TV DB #####
class Tv(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    resolution = db.Column(db.String(100), nullable=False)
    usb = db.Column(db.String(100), nullable=False)
    wifi = db.Column(db.String(100), nullable=False)
    smart = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product('{self.productid}','{self.brand}','{self.color}','{self.size}', '{self.resolution}',  '{self.usb}', '{self.wifi}', '{self.smart}')"


##### LAPTOP DB #####
class Laptop(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    ram_size = db.Column(db.Integer, nullable=False)
    hdd_size = db.Column(db.Integer, nullable=False)
    ssd_size = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    disp_size = db.Column(db.String(100), nullable=False)
    resolution = db.Column(db.String(100), nullable=False)
    os = db.Column(db.String(100), nullable=False)
    processor = db.Column(db.String(100), nullable=False)
    camera = db.Column(db.String(100), nullable=False)
    touch = db.Column(db.String(100), nullable=False)
    battery = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product('{self.productid}','{self.brand}','{self.ram_size}','{self.hdd_size}', '{self.ssd_size}',  '{self.color}', '{self.disp_size}', '{self.resolution}','{self.os}', '{self.processor}', '{self.camera}', '{self.touch}', '{self.battery}')"


##### REFRIGERATOR DB #####
class Refrigerator(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    doors = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    ice_dispencer = db.Column(db.String(15), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    energy_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product('{self.productid}','{self.brand}','{self.doors}','{self.color}', '{self.capacity}',  '{self.ice_dispencer}', '{self.weight}', '{self.energy_rating}')"


##### WASHING MACHINE DB #####
class WashingMachine(db.Model):
    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    load_type = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    automatic = db.Column(db.String(100), nullable=False)
    energy_rating = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Product('{self.productid}','{self.brand}','{self.weight}','{self.color}', '{self.load_type}',  '{self.capacity}', '{self.automatic}', '{self.energy_rating}')"


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
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    # productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    ordered_quantity = db.Column(db.Integer, nullable=False)
    ordered_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    order_state = db.Column(db.String(50),nullable=False,default='Shipped')

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}', '{self.ordered_quantity}' , '{self.ordered_date}', '{self.order_state}')"



##### ROUTES #####

if __name__=='__main__':
    app.run(debug=True)
            
