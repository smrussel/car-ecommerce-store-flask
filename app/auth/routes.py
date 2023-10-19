from flask import Blueprint, render_template, flash, \
    redirect, url_for, request, session
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordForm, ResetPasswordRequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TradeModel
from app import db
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_url = request.args.get('next')
        if current_user.admin:
            return redirect(next_url or url_for('admin_bp.admin_panel'))
        return redirect(next_url or url_for('auth.dashboard'))
    return render_template('cars/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data.lower(),
            last_name=form.last_name.data.lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('cars/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    # session.clear()
    flash("You've signed out!", "success")
    return redirect(url_for('main.index'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occured, please try again', 'danger')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        model = request.form.get('model')
        make = request.form.get('make')
        year = request.form.get('year')
        mileage = request.form.get('mileage')
        comments = request.form.get('comments')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        zip = request.form.get('zip')
        user_id = current_user.id
        # print(model,make,year,mileage,comments,email,first_name,last_name,phone,zip,user_id)
        if year and model and make and mileage and first_name and last_name and email and phone and zip and comments:
            trade_requested = TradeModel(
                year=year, model=model, make=make, mileage=mileage, first_name=first_name,
                last_name=last_name, phone=phone, zip=zip, comments=comments, email=email,
                user_id=user_id
            )
            db.session.add(trade_requested)
            db.session.commit()
            flash('Your Trade in request submitted', 'success')
            return render_template('cars/trade_success.html')
    return render_template('cars/dashboard.html')
