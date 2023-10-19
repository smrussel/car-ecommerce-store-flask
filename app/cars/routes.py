from flask import Blueprint, render_template, flash, \
    redirect, url_for, request, session
from app.models import Car
from sqlalchemy import func
from .forms import ReviewForm
from app import db
from app.models import Review
from flask_login import current_user, login_required

cars = Blueprint('cars', __name__)


@cars.route('/all-cars')
def cars_page():
    page = request.args.get('page', 1, type=int)
    cars = Car.query.order_by(Car.created_at.desc()).filter_by(available=True).paginate(
        page=page,
        per_page=6)
    query = Car.query.with_entities(Car.model).distinct().all()
    models = [i[0] for i in query]
    query = Car.query.with_entities(Car.make).distinct().all()
    makes = [i[0] for i in query]
    query = Car.query.with_entities(Car.color).distinct().all()
    colors = [i[0] for i in query]
    return render_template('cars/all-cars.html', all_cars=cars, model_search=models, make_search=makes,
                           color_search=colors)


@cars.route('/car-detail/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('cars/car-detail.html', car=car)


@cars.route('/search')
def car_search():
    query = Car.query.with_entities(Car.model).distinct().all()
    models = [i[0] for i in query]
    query = Car.query.with_entities(Car.make).distinct().all()
    makes = [i[0] for i in query]
    query = Car.query.with_entities(Car.color).distinct().all()
    colors = [i[0] for i in query]
    query = Car.query.with_entities(Car.year).distinct().all()
    years = [i[0] for i in query]
    query = Car.query.with_entities(Car.gearbox).distinct().all()
    gearboxes = [i[0] for i in query]

    cars = Car.query.order_by(Car.created_at.desc())

    if 'name' in request.args:
        car_title = request.args.get('name')
        if car_title:
            cars = cars.filter(Car.car_title.contains(car_title))

    if 'model' in request.args:
        model = request.args.get('model')
        if model:
            cars = cars.filter(Car.model == model)

    if 'year' in request.args:
        year = request.args.get('year')
        if year:
            cars = cars.filter(Car.year == year)

    if 'gearbox' in request.args:
        gearbox = request.args.get('gearbox')
        if gearbox:
            cars = cars.filter(Car.gearbox == gearbox)

    if 'make' in request.args:
        make = request.args.get('make')
        if make:
            cars = cars.filter(Car.make == make)

    if 'color' in request.args:
        color = request.args.get('color')
        if color:
            cars = cars.filter(Car.color == color)

    if 'min_price' in request.args:
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        print(min_price, max_price)
        if max_price:
            cars = cars.filter(Car.price.between(min_price, max_price))

    cars = cars.all()

    return render_template('cars/search.html', cars=cars, model_search=models,
                           make_search=makes, color_search=colors, year_search=years, transmission_search=gearboxes)


@cars.route('/reviews')
def all_car_reviews():
    page = request.args.get('page', 1, type=int)
    cars = Car.query.order_by(Car.created_at.desc()).paginate(
        page=page,
        per_page=6)
    query = Car.query.with_entities(Car.model).distinct().all()
    models = [i[0] for i in query]
    query = Car.query.with_entities(Car.make).distinct().all()
    makes = [i[0] for i in query]
    query = Car.query.with_entities(Car.color).distinct().all()
    colors = [i[0] for i in query]
    return render_template('cars/all-car-reviews.html', all_cars=cars, model_search=models, make_search=makes,
                           color_search=colors)


@cars.route('/review/<int:car_id>', methods=['GET', 'POST'])
def car_review(car_id):
    car = Car.query.get(car_id)
    form = ReviewForm()
    temp = db.session.query(func.avg(Review.rating).label('average')).filter(Review.car_id == car_id)
    if temp[0].average:
        avg = round(temp[0].average, 2)
    else:
        avg = 0

    if form.validate_on_submit():
        rev = Review.query.filter_by(car_id=car_id, user_id=current_user.get_id()).count()
        if rev != 0:
            flash("Can't review a car twice. Please edit/update your previous review", "danger")
        else:
            review = Review(
                rating=round(form.rating.data, 2),
                text=form.text.data,
                user_id=current_user.get_id(),
                car_id=car_id
            )
            flash("Review has been added", "success")
            db.session.add(review)
            db.session.commit()
        return redirect(url_for('cars.car_review', car_id=car_id))
    return render_template('cars/car-review.html', car=car, form=form, average=avg)


@cars.route('/edit-review/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_review(car_id):
    review = Review.query.filter_by(car_id=car_id, user_id=current_user.get_id())[0]
    form = ReviewForm()
    if request.method == 'GET':
        form.text.data = review.text
    if form.validate_on_submit() and request.method == 'POST':
        review.rating = round(form.rating.data, 2)
        review.text = form.text.data
        db.session.commit()
        return redirect(url_for('cars.car_review', car_id=car_id))
    return render_template('cars/edit_review.html', form=form)


@cars.route('/review/<id1>/delete_review/<id2>')
@login_required
def delete_review(id1, id2):
    if Review.query.filter_by(id=id2).delete():
        db.session.commit()
        flash('Review has been deleted', 'success')
        return redirect(url_for('cars.car_review', car_id=id1))
    return redirect(url_for('cars.car_review', car_id=id1))


