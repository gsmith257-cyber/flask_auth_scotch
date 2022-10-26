# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
def profile():
    if current_user.username == 'admin':
        return render_template('admin.html', name=current_user.name)
    else:
        return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/manufacturing')
def manufacturing():
    return render_template('manufacturing.html')

@main.route('/solar')
def solar():
    return render_template('solar.html')
