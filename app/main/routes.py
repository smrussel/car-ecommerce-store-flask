from app.models import Car

from flask import Blueprint, render_template, redirect, url_for, request

main = Blueprint('main', __name__)


@main.route('/')
def index():
    cars = Car.query.order_by(Car.created_at.desc()).filter_by(available=True)
    query = Car.query.with_entities(Car.model).distinct().all()
    models = [i[0] for i in query]
    query = Car.query.with_entities(Car.make).distinct().all()
    makes = [i[0] for i in query]
    query = Car.query.with_entities(Car.color).distinct().all()
    colors = [i[0] for i in query]
    print(models, makes, colors)
    return render_template('cars/index.html', all_cars=cars,model_search=models,make_search=makes,color_search=colors)
