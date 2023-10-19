from flask import (render_template, session, request, redirect, url_for,
                   flash, Blueprint)

from app.models import CarReserve, ReserveModel, CustomerOrderModel, OrderProductModel,Car,User
from flask_login import login_required, current_user
from .forms import CarReserveForm
import uuid
from app import db
import secrets

checkout = Blueprint("checkout", __name__)


@checkout.route('/checkout')
@login_required
def checkout_page():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.index'))
    subtotal = 0
    grand_total = 0
    tax = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.06 * float(subtotal)))
        grand_total = float("%.2f" % (1.06 * subtotal))
    return render_template('cars/checkout.html', tax=tax, grandtotal=grand_total)


@checkout.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve_page():
    form = CarReserveForm()
    for key, product in session['Shoppingcart'].items():
        print(key, product)
    if form.validate_on_submit():
        reference = None
        try:
            reference = str(uuid.uuid4())
            reserve = ReserveModel(reference_number=reference, user_id=current_user.get_id())
            db.session.add(reserve)
            db.session.commit()
            for key, product in session['Shoppingcart'].items():
                print(key, product)
                res = CarReserve.query.filter_by(car_id=key, user_id=current_user.get_id()).count()
                if res != 0:
                    flash(f"{res.car.car_title} Can't reserve a car twice.", "danger")
                else:
                    get_car = Car.query.get(key)
                    get_car.available = False
                    reserve_car = CarReserve(
                        name=form.name.data,
                        address=form.address.data,
                        email=form.email.data,
                        phone_number=form.phone_number.data,
                        user_id=current_user.get_id(),
                        car_id=key,
                        reserve=reserve
                    )
                    db.session.add(reserve_car)
                    db.session.commit()
            session.pop('Shoppingcart')

            if reference:
                flash("Reservation done.", "success")
                return render_template('cars/reservation_success.html', reference=reference)
            else:
                return redirect(url_for('cars.cars_page'))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('cars.cars_page'))
    return render_template('cars/reserve_form.html', form=form)


@checkout.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        user_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrderModel(invoice=invoice, user_id=user_id)
            db.session.add(order)
            db.session.commit()
            for key, product in session['Shoppingcart'].items():
                print(key, product)
                get_car = Car.query.get(key)
                get_car.available = False
                order_product = OrderProductModel(user_id=user_id, order=order,
                                                  car=get_car,
                                                  car_title=product['name'],
                                                  quantity=int(product['quantity']),
                                                  price=float(product['price']),
                                                  color=product['color'])
                db.session.add(order_product)
                db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('checkout.orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('cart_bp.get_cart'))


# this one you call when you wan to view the order page
@checkout.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        tax = 0
        total_point = 0
        user_id = current_user.id
        customer = User.query.filter_by(id=user_id).first()
        customer_order = CustomerOrderModel.query.filter_by(user_id=user_id, invoice=invoice).order_by(
            CustomerOrderModel.id.desc()).first()
        for order in customer_order.orders:
            subTotal += float(order.price) * order.quantity
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('auth.login'))
    return render_template('cars/order.html', invoice=invoice, tax=tax, subTotal=subTotal,
                           grandTotal=grandTotal, customer=customer, customer_order=customer_order)

