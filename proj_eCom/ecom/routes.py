from flask import render_template, url_for, flash, redirect, request
from ecom import app, db
from ecom.models import User, Product,Cart,Order
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os


@app.route('/')
def root():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	else:
		return redirect(url_for('home'))

##### HOME PAGE #####
@app.route('/home')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	product=Product.query.all()
	return render_template('home.html',title='home',products=product)
	# return render_template('home.html',title='home')

##### SIGN UP PAGE #####
@app.route('/signup',methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		flash("First logout inorder to signup!",'primary')
		return redirect(url_for('index'))
	if request.method=='POST':
		user=User(username=request.form['username'],email=request.form['email'],password=request.form['password'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('signup.html',title='signup')

##### LOGIN PAGE #####
@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	error=None
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		user = User.query.filter_by(email=email).first()
		if user and user.password==password:
			login_user(user)
			flash('You are logged in','success')
			return redirect(url_for('index'))
		else:
			error = 'Invalid username or password. Please try again!'
			flash('Invalid email or Password!','danger')
		return redirect(url_for('home'))
	return render_template('login.html',title='login',error=error)


##### INDEX PAGE #####
@login_required
@app.route('/index')
def index():
	product=Product.query.all()
	return render_template('index.html',title='index',products=product)
	# return render_template('index.html',title='index')

##### LOGOUT PAGE #####
@login_required
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

##### MY CART PAGE #####
@login_required
@app.route('/cart')
def cart():
	##change made ##
	userid=current_user.id
	cart=Cart.query.filter_by(id=userid).all()
	if cart :
		# product=Product.query.filter_by(productid=cart.productid).all()
		product=[]
		for c in cart:			
			p=Product.query.filter_by(productid=c.productid).first()
			product.append(p)
		return render_template('cart.html',product=product)
	else:
		flash('Your cart is Empty ','warning')
		return redirect(url_for('index'))


##### ADD GADGET TO HOME AND INDEX #####
'''it is done directly by entering data of products into db'''

##### ADD GADGET TO CART #####
@login_required
@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
	if request.method=='POST':
		productid=request.form['productid']
		quantity=15
		userid=current_user.id
		cart=Cart(id=userid,productid=productid,quantity=quantity)
		cart1=Cart.query.filter_by(id=userid,productid=productid).first()
		if cart1 :
			flash('Item already in cart!','warning')
			return redirect(url_for('index'))	
		else:
			db.session.add(cart)
			db.session.commit()
			flash('Item added to cart succesfully!','success')
			return redirect(url_for('index'))
	# return render_template('cart.html',title='cart')

##### PLACE ORDER FROM CART #####
@login_required
@app.route('/place_order',methods=['GET','POST'])
def place_order():
	try:
		if request.method=='POST':
			productid=request.form['productid']
			quantity=1
			userid=current_user.id
			order=Order(id=userid,productid=productid,quantity=quantity)
			db.session.add(order)
			# raise ValueError("Some Inegrity Constraint Error Happened")
			# db.session.add(order)
			db.session.commit()
			flash('Placed order for item succesfully!','success')
			cart=Cart.query.filter_by(id=userid,productid=productid,quantity=quantity)
			# db.session.delete(cart)
			cart.delete()
			db.session.commit()
			flash('Item removed from your cart!','success')
			return redirect(url_for('index'))
		# return render_template('cart.html',title='cart')
	except :
		flash('Cannot place order, as Item already is in cart!','warning')
		return redirect(url_for('cart'))


##### MY ORDERS PAGE #####
@login_required
@app.route('/orders')
def orders():
	userid=current_user.id
	order=Order.query.filter_by(id=userid).all()
	if order :
		product=[]
		for o in order:				
			p=Product.query.filter_by(productid=o.productid).first()
			product.append(p)
		return render_template('orders.html',product=product,order=order,title='orders')
	else:
		flash('You have no orders yet! ','warning')
		return redirect(url_for('index'))

##### PAYMENT PAGE #####
@login_required
@app.route('/payment',methods=['GET','POST'])
def payment():
	flash('Make your payment!','primary')
	return render_template('payment.html',title='payment')


##### FEEDBACK PAGE #####
@login_required
@app.route('/feedback',methods=['GET','POST'])
def feedback():
	return render_template('feedback.html',title='feedback')

'''TEST ROUTES'''
##### description PAGE #####
@login_required
@app.route("/details/<string:pid>",methods=['GET','POST'])
def details(pid):
	product=Product.query.filter_by(productid=pid).first()
	return render_template('details.html',title='details',products=product)


