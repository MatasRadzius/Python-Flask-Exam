from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, JoinGroupForm, AddBillForm
from models import User, Group, GroupUser, Bill
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome, you are now logged in!',
            'success')
            return redirect(url_for('group'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/group", methods=['GET', 'POST'])
def group():
    form = JoinGroupForm()
    group = None
    if form.validate_on_submit():
        group = Group.query.filter_by(id=form.group_id.data, name=form.group_name.data).first()
        if group:
            group_user = GroupUser(user_id=session['user_id'], group_id=group.id)
            db.session.add(group_user)
            db.session.commit()
            flash('You have successfully joined the group!', 'success')
            return redirect(url_for('group'))
        else:
            flash('Group not found. Please check the group ID and name.', 'danger')
    user_groups = GroupUser.query.filter_by(user_id=session['user_id']).all()
    groups = [Group.query.get(group_user.group_id) for group_user in user_groups]
    return render_template('group.html', groups=groups, form=form, group=group)



@app.route('/bills/<int:group_id>', methods=['GET', 'POST'])
def bills(group_id):
    bills_data = Bill.query.filter_by(group_id=group_id).all()
    form = AddBillForm()
    
    if form.validate_on_submit():
        new_bill = Bill(description=form.description.data, amount=form.amount.data, group_id=group_id)
        db.session.add(new_bill)
        db.session.commit()
        flash('Bill added successfully!')
        return redirect(url_for('bills', group_id=group_id))
    
    return render_template('bills.html', bills=bills_data, form=form, group_id=group_id)



@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

