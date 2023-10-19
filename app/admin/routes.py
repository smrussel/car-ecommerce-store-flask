from flask import Blueprint, render_template, flash, \
    redirect, url_for, request, session, current_app

from .forms import PostForm, CarForm, FaqForm, UpdateUserForm
from app.models import Car, Blog, FaqModel, User,TradeModel
from app import db, photos
import secrets
from .utils import admin_only
import os

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin-panel', methods=['GET', 'POST'])
@admin_only
def admin_panel():
    return render_template('admin/admin.html')


@admin_bp.route('/view-cars', methods=['GET', 'POST'])
@admin_only
def view_cars():
    cars = Car.query.order_by(Car.created_at.desc()).all()
    return render_template('admin/admin-cars.html', cars=cars)


@admin_bp.route('/view-users', methods=['GET', 'POST'])
@admin_only
def view_users():
    users = User.query.all()
    return render_template('admin/admin-users.html', users=users)


@admin_bp.route('/view-faqs', methods=['GET', 'POST'])
@admin_only
def view_faqs():
    faqs = FaqModel.query.order_by(FaqModel.created_at.desc()).all()
    return render_template('admin/admin-faqs.html', faqs=faqs)


@admin_bp.route('/view-blogs', methods=['GET', 'POST'])
@admin_only
def view_blogs():
    posts = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('admin/admin-blogs.html', posts=posts)

@admin_bp.route('/view-trades', methods=['GET', 'POST'])
@admin_only
def view_trades():
    trades = TradeModel.query.order_by(TradeModel.created_at.desc()).all()
    return render_template('admin/admin-trades.html', trades=trades)


@admin_bp.route('/update-user/<int:user_id>', methods=['GET', 'POST'])
@admin_only
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        admin=user.admin
    )
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.username = form.username.data
        user.email = form.email.data
        user.admin = form.admin.data
        db.session.commit()

        return redirect(url_for("admin_bp.view_users"))
    return render_template('admin/create-post.html', form=form, title="Update User")


@admin_bp.route('/update-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def update_post(post_id):
    post = Blog.query.get_or_404(post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        if request.files.get('img_url'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + post.img_url))
                post.img_url = photos.save(request.files.get('img_url'), name=secrets.token_hex(10) + ".")
            except:
                post.img_url = photos.save(request.files.get('img_url'), name=secrets.token_hex(10) + ".")
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for("admin_bp.view_blogs"))
    return render_template('admin/create-post.html', form=form, title="Update Post")


@admin_bp.route('/update-faq/<int:faq_id>', methods=['GET', 'POST'])
@admin_only
def update_faq(faq_id):
    faq = FaqModel.query.get_or_404(faq_id)
    form = FaqForm(
        question=faq.question,
        answer=faq.answer
    )
    if form.validate_on_submit():
        faq.question = form.question.data
        faq.answer = form.answer.data
        db.session.commit()
        return redirect(url_for("admin_bp.view_faqs"))
    return render_template('admin/create-faq.html', form=form, title="Update FAQ")


@admin_bp.route('/update-car/<int:car_id>', methods=['GET', 'POST'])
@admin_only
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(
        car_title=car.car_title,
        country=car.country,
        city=car.city,
        color=car.color,
        make=car.make,
        model=car.model,
        reg_no=car.reg_no,
        year=car.year,
        price=car.price,
        gearbox=car.gearbox,
        description=car.description,
        car_photo=car.car_photo,
        car_photo_1=car.car_photo_1,
        car_photo_2=car.car_photo_2,
        car_photo_3=car.car_photo_3,
        car_photo_4=car.car_photo_4,
        miles=car.miles,
        mileage=car.mileage,
        fuel_type=car.fuel_type,
    )
    if form.validate_on_submit():
        car.car_title = form.car_title.data
        car.country = form.country.data
        car.city = form.city.data
        car.color = form.color.data
        car.make = form.make.data
        car.model = form.model.data
        car.reg_no = form.reg_no.data
        car.year = form.year.data
        car.price = form.price.data
        car.gearbox = form.gearbox.data
        car.description = form.description.data
        car.miles = form.miles.data
        car.mileage = form.mileage.data
        car.fuel_type = form.fuel_type.data

        if request.files.get('car_photo'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + car.car_photo))
                car.car_photo = photos.save(request.files.get('car_photo'), name=secrets.token_hex(10) + ".")
            except:
                car.car_photo = photos.save(request.files.get('car_photo'), name=secrets.token_hex(10) + ".")

        if request.files.get('car_photo_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + car.car_photo_1))
                car.car_photo_1 = photos.save(request.files.get('car_photo_1'), name=secrets.token_hex(10) + ".")
            except:
                car.car_photo_1 = photos.save(request.files.get('car_photo_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('car_photo_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + car.car_photo_2))
                car.car_photo_2 = photos.save(request.files.get('car_photo_2'), name=secrets.token_hex(10) + ".")
            except:
                car.car_photo_2 = photos.save(request.files.get('car_photo_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('car_photo_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + car.car_photo_3))
                car.car_photo_3 = photos.save(request.files.get('car_photo_3'), name=secrets.token_hex(10) + ".")
            except:
                car.car_photo_3 = photos.save(request.files.get('car_photo_3'), name=secrets.token_hex(10) + ".")

        if request.files.get('car_photo_4'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploaded-images/" + car.car_photo_4))
                car.car_photo_4 = photos.save(request.files.get('car_photo_4'), name=secrets.token_hex(10) + ".")
            except:
                car.car_photo_4 = photos.save(request.files.get('car_photo_4'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        return redirect(url_for("admin_bp.view_cars"))
    return render_template('admin/create-car.html', form=form, title="Update Car")


@admin_bp.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
@admin_only
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("admin_bp.view_users"))


@admin_bp.route('/delete-car/<int:car_id>', methods=['GET', 'POST'])
@admin_only
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for("admin_bp.view_cars"))


@admin_bp.route('/delete-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def delete_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("admin_bp.view_blogs"))


@admin_bp.route('/delete-faq/<int:faq_id>', methods=['GET', 'POST'])
@admin_only
def delete_faq(faq_id):
    faq = FaqModel.query.get_or_404(faq_id)
    if faq:
        db.session.delete(faq)
        db.session.commit()
        return redirect(url_for("admin_bp.view_faqs"))


@admin_bp.route('/create-car', methods=['GET', 'POST'])
@admin_only
def create_car():
    form = CarForm()
    if form.validate_on_submit():
        car_photo = photos.save(request.files.get('car_photo'), name=secrets.token_hex(10) + ".")
        car_photo_1 = photos.save(request.files.get('car_photo_1'), name=secrets.token_hex(10) + ".")
        car_photo_2 = photos.save(request.files.get('car_photo_2'), name=secrets.token_hex(10) + ".")
        car_photo_3 = photos.save(request.files.get('car_photo_3'), name=secrets.token_hex(10) + ".")
        car_photo_4 = photos.save(request.files.get('car_photo_4'), name=secrets.token_hex(10) + ".")

        new_car = Car(car_title=form.car_title.data, country=form.country.data, city=form.city.data,
                      color=form.color.data, model=form.model.data, make=form.make.data, year=form.year.data,
                      price=form.price.data, description=form.description.data, miles=form.miles.data,
                      mileage=form.mileage.data, fuel_type=form.fuel_type.data,
                      car_photo=car_photo, car_photo_1=car_photo_1, car_photo_2=car_photo_2, car_photo_3=car_photo_3,
                      car_photo_4=car_photo_4, gearbox=form.gearbox.data, reg_no=form.reg_no.data)
        db.session.add(new_car)
        db.session.commit()
        flash("Successfully Added Car.", category='success')
        return redirect(url_for("cars.cars_page"))
    return render_template('admin/create-car.html', form=form, title="Add Car")


@admin_bp.route('/create-post', methods=['GET', 'POST'])
@admin_only
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        img_url = photos.save(request.files.get('img_url'), name=secrets.token_hex(10) + ".")
        new_post = Blog(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=img_url
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blogs.all_blogs"))
    return render_template('admin/create-post.html', form=form, title="Add Post")


@admin_bp.route('/create-faq', methods=['GET', 'POST'])
@admin_only
def create_faq():
    form = FaqForm()
    if form.validate_on_submit():
        faq = FaqModel(question=form.question.data, answer=form.answer.data)
        db.session.add(faq)
        db.session.commit()
        return redirect(url_for("pages.faq"))
    return render_template('admin/create-faq.html', form=form, title="Add FAQ")
