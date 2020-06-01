from flask import render_template, url_for, flash, redirect, request
from ecom import app, db
from ecom.models import *
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

##### HOME PAGE #####
@app.route('/')
def home():
	return render_template('home.html',title='home')


##### SIGN UP PAGE #####
@app.route('/signup',methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		flash("First logout inorder to signup!",'warning')
		return redirect(url_for('home'))
	if request.method=='POST':
		user=User(username=request.form['username'],email=request.form['email'],phno=request.form['phno'],password=request.form['password'])
		db.session.add(user)
		db.session.commit()
		flash('Registered succesfully!','success')
		return redirect(url_for('login'))		
	return render_template('signup.html',title='signup')

##### LOGIN PAGE #####
@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	error=None
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		user = User.query.filter_by(email=email).first()
		if user and user.password==password:
			login_user(user)
			flash('You are logged in','success')
			return redirect(url_for('home'))
		else:
			error = 'Invalid username or password. Please try again!'
			flash('Invalid email or Password!','danger')
		return redirect(url_for('home'))
	return render_template('login.html',title='login',error=error)

##### ABOUT US PAGE #####
@app.route('/about')
def about():
	return render_template('about.html',title='about')

##### HELP PAGE #####
@app.route('/help')
def help():
	return render_template('help.html',title='help')

##### A/C RECOVERY PAGE #####
@app.route('/ac_recovery',methods=['GET','POST'])
def ac_recovery():
	if request.method=='POST':
		email=request.form['email']
		user = User.query.filter_by(email=email).first()
		if user:
			flash('A recovery mail has been sent to your inbox. Please Check!','success')
			return redirect(url_for('ac_recovery'))
		else:
			flash('This email has not been registered yet. Please Signup first!','danger')
			return redirect(url_for('signup'))
	return render_template('ac_recovery.html',title='ac_recovery')


##### INDEX PAGE #####
@login_required
@app.route('/index/<string:catogery>',methods=['GET','POST'])
def index(catogery):
	product=Product.query.filter_by(catogery=catogery)
	return render_template('index.html',title='index',products=product,catogery=catogery)

##### LOGOUT PAGE #####
@login_required
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

##### USER PROFILE PAGE #####
@login_required
@app.route('/user_ac')
def user_ac():
	uid=current_user.id
	user=User.query.filter_by(id=uid).first()
	return render_template('user_ac.html',title='user_ac',user=user)

##### MY CART PAGE #####
@login_required
@app.route('/cart')
def cart():
	##change made ##
	userid=current_user.id
	cart=Cart.query.filter_by(id=userid).all()
	subtot=0
	shipping=10
	tax=5
	if cart :
		# product=Product.query.filter_by(productid=cart.productid).all()
		product=[]
		for c in cart:			
			p=Product.query.filter_by(productid=c.productid).first()
			subtot+=p.discounted_price
			product.append(p)
		tot=subtot+shipping+tax
		return render_template('cart.html',product=product,cart=cart,subtot=subtot,tot=tot)
	else:
		flash('Your cart is Empty ','warning')
		return redirect(url_for('home'))


##### ADD GADGET TO HOME AND INDEX #####
'''it is done directly by entering data of products into db'''

##### ADD GADGET TO CART #####
@login_required
@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
	if request.method=='POST':
		productid=request.form['productid']
		quantity=request.form['quantity']
		userid=current_user.id
		cart=Cart(id=userid,productid=productid,quantity=quantity)
		cart1=Cart.query.filter_by(id=userid,productid=productid).first()
		if cart1 :
			flash('Item already in cart!','warning')
			return redirect(url_for('home'))	
		else:
			db.session.add(cart)
			db.session.commit()
			flash('Item added to cart succesfully!','success')
			return redirect(url_for('home'))

##### DELETE GADGET FROM CART #####
# @login_required
# @app.route('/del_from_cart/<string:pid>',methods=['GET','POST'])
# def del_from_cart(pid):
# 	# if request.method=='POST':
# 	userid=current_user.id
# 	quantity=1
# 	cart=Cart(id=userid,productid=pid,quantity=quantity)
# 	cart1=Cart.query.filter_by(id=userid,productid=pid).first()
# 	if cart1 :
# 		Cart.query.filter(id==userid and productid==pid).delete()
# 		# db.session.rollback()
# 		# db.session.commit()
# 		# db.session.flush()
# 		flash('Item deleted from cart!','success')
# 		return redirect(url_for('cart'))
# 	else:
# 		flash('Item not in cart!','danger')
# 		return redirect(url_for('cart'))
# 		# return redirect(url_for('cart'))
# 	# return render_template('cart.html',title='cart')



##### PLACE ORDER FROM CART #####
@login_required
@app.route('/place_order',methods=['GET','POST'])
def place_order():
	try:
		if request.method=='POST':
			userid=current_user.id
			order_state='Out For Delivery'
			cart=Cart.query.filter_by(id=userid)
			if cart:
				for c in cart:
					order_id=c.productid
					ordered_quantity=c.quantity
					order=Order(id=userid,order_id=order_id,ordered_quantity=ordered_quantity,order_state=order_state)
					db.session.add(order)
					'''del from cart'''
					# cart=Cart.query.filter_by(id=userid,productid=productid,quantity=quantity)
					# cart.delete()
					# db.session.commit()
					# flash('Item removed from your cart!','success')		
				db.session.commit()
				flash('Placed order for item succesfully!','success')	
				return redirect(url_for('home'))
			else:
				flash('Cannot place order, No items in Cart!','danger')	
				return redirect(url_for('home'))
	except :
		flash('Cannot place order, as Item already ordered!','warning')
		return redirect(url_for('cart'))


##### MY ORDERS PAGE #####
@login_required
@app.route('/orders')
def orders():
	userid=current_user.id
	order=Order.query.filter_by(id=userid).all()
	if order :
		product=Product.query.all()
		return render_template('orders.html',product=product,order=order,title='orders')

	else:
		flash('You have no orders yet! ','warning')
		return redirect(url_for('home'))

##### PAYMENT PAGE #####
@login_required
@app.route('/payment',methods=['GET','POST'])
def payment():
	userid=current_user.id
	cart=Cart.query.filter_by(id=userid).all()
	subtot=0
	shipping=10
	tax=5
	if cart :
		for c in cart:			
			p=Product.query.filter_by(productid=c.productid).first()
			subtot+=p.discounted_price
		tot=subtot+shipping+tax
	# product=Product.query.all()
	flash('Make your payment!','home')
	return render_template('payment.html',title='payment',subtot=subtot,tot=tot)


##### FEEDBACK PAGE  #####
@login_required
@app.route('/feedback',methods=['GET','POST'])
def feedback():
	return render_template('feedback.html',title='feedback')

##### FEEDBACK Submit Redirect #####
@login_required
@app.route('/feedback_submit',methods=['GET','POST'])
def feedback_submit():
	flash('Your response have been recorded','success')
	return redirect(url_for('feedback'))

'''TEST ROUTES'''
##### description PAGE #####
# @login_required
@app.route("/details/<string:catogery>/<string:pid>",methods=['GET','POST'])
def details(catogery,pid):
	product=Product.query.filter_by(productid=pid).first()
	if catogery=='Mobile':
		features=Mobile.query.filter_by(productid=pid).first()
	elif catogery=='Laptop':
		features=Laptop.query.filter_by(productid=pid).first()
	elif catogery=='Tv':
		features=Tv.query.filter_by(productid=pid).first()
	elif catogery=='Refrigerator':
		features=Refrigerator.query.filter_by(productid=pid).first()
	elif catogery=='WashingMachine':
		features=WashingMachine.query.filter_by(productid=pid).first()
	else:
		flash('Invalid Request!',danger)
		return redirect(url_for('home'))

	return render_template('details.html',title='details',products=product,catogery=catogery,features=features)

