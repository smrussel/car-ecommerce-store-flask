from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session

from app.models import FaqModel
pages = Blueprint('pages', __name__)


@pages.route('/contact')
def contact():
    return render_template('pages/contact.html')


@pages.route('/about')
def about():
    return render_template('pages/about.html')


@pages.route('/faq')
def faq():
    faqs = FaqModel.query.all()
    return render_template('pages/faq.html', faqs=faqs)
