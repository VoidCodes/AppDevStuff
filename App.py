from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from dbconfig import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models import User

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

#Import models after db is initialized
from models import Product, User, Order, OrderItem

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('User/Home.html')

@app.route("/shop")
def shop():
    try:
        allproducts = Product.query.all()
    except SQLAlchemyError as e:
        flash('Error: %s' % e, 'error')
        allproducts = []
    return render_template('User/shop.html', products=allproducts)


@app.route("/register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        """
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        user = "INSERT INTO user (username, password) VALUES ('%s', '%s')" % (username, password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('/'))
        """
        username = request.form['username']
        password = request.form['password']
        try:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('User created successfully', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            flash('Error: %s' % e, 'error')
            return redirect(url_for('signup'))
        
    return render_template('User/register.html')


if __name__ == "__main__":
    app.run(debug=True)
