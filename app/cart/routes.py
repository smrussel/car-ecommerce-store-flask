from flask import (render_template, session, request, redirect, url_for,
                   flash, Blueprint)

from app.models import Car


cart_bp = Blueprint("cart_bp", __name__)


def merger_dicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@cart_bp.route('/add-cart', methods=['POST'])
def add_cart():
    try:
        car_id = request.form.get('car_id')
        quantity = int(request.form.get('quantity'))
        car = Car.query.filter_by(id=car_id).first()
        print(car_id, quantity, car.car_title)
        if request.method == "POST":
            dict_items = {car_id: {'name': car.car_title, 'price': float(car.price),
                                   'color': car.color, 'quantity': quantity, 'image': car.car_photo}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if car_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(car_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = merger_dicts(session['Shoppingcart'], dict_items)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = dict_items
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@cart_bp.route('/update-cart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.index'))

    quantity = request.form.get('quantity')
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == code:
                item['quantity'] = quantity
                flash('Item is updated!')
                return redirect(url_for('cart_bp.get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart_bp.get_cart'))


@cart_bp.route('/cart')
def get_cart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.index'))
    subtotal = 0
    grand_total = 0
    tax = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.06 * float(subtotal)))
        grand_total = float("%.2f" % (1.06 * subtotal))
    return render_template('cars/cart.html', tax=tax, grandtotal=grand_total)




@cart_bp.route('/delete-item/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.index'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('cart_bp.get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart_bp.get_cart'))


@cart_bp.route('/clear-cart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('cars.cars_page'))
    except Exception as e:
        print(e)

