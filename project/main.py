# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os
import re
import ftplib

HOSTNAME = "10.0.40.73"
USERNAME = "blueteam"
PASSWORD = "Blueteam2022"
ftp_server = ftplib.FTP(HOSTNAME)
ftp_server.login('anonymous')
ftp_server.encoding = "utf-8"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
def profile():
    if current_user.name == 'admin':
        return render_template('admin.html', name=current_user.name)
    else:
        return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@auth.route('/contact', methods=['POST'])
def contact_post():
    file = request.form.get('file')
    #get the file name
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    #prevent LFI
    if re.search(r'(\.\.)|[/\\]', name):
        flash('Invalid name')
        return redirect(url_for('main.contact'))
    else:
        #save file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        #upload file
        ftp_server.storbinary('STOR ' + file.filename, open(file.filename, 'rb'))
        return redirect(url_for('main.contact'))

@main.route('/manufacturing')
def manufacturing():
    return render_template('manufacturing.html')

@main.route('/solar')
def solar():
    return render_template('solar.html')
