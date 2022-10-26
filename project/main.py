# main.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import re
import ftplib

HOSTNAME = "10.0.40.73"
USERNAME = "anonymous"
PASSWORD = "anonymous"
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
def profile():
    if current_user.name == 'admin':
        #get list of files
        ftp_server.cwd("/")
        #get list of files
        files = []
        allThings = ftp_server.nlst()
        for file in allThings:
            try:
                ftp_server.cwd(file)
                ftp_server.cwd('../')
            except:
                files += [file]
        return render_template('admin.html', name=current_user.name, files=files)

    else:
        return render_template('index.html')

#create download route
@main.route('/download/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    if current_user.name == 'admin':
        upload_folder = "uploads/"
        #empty the uploads folder
        for file in os.listdir(upload_folder):
            os.remove(upload_folder + file)
        if re.search(r'(\.\.)|[/\\]', filename):
            flash('Invalid name')
            return redirect(url_for('main.admin'))
        ftp_server.cwd('/')
        files = ftp_server.nlst()
        if filename in files:
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
            with open(os.path.join(upload_folder, filename), "wb") as file:
                ftp_server.retrbinary('RETR ' + filename, file.write)
            return send_file(os.path.join(os.getcwd(), upload_folder, filename), as_attachment=True)
        else:
            return redirect(url_for('main.profile'))
    else:
        return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/contact', methods=['POST'])
def contact_post():
    #get the file from the form
    file = request.files['file']
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    #prevent LFI
    if re.search(r'(\.\.)|[/\\]', file.filename):
        flash('Invalid name')
        return redirect(url_for('main.contact'))
    else:
        upload_folder = "uploads/"
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)
        file.save(os.path.join(upload_folder, file.filename))
        #upload file
        with open(os.path.join(upload_folder, file.filename), 'rb') as f:
            ftp_server.storbinary('STOR ' + file.filename, f)
        #remove file
        os.remove(os.path.join(upload_folder, file.filename))
        return redirect(url_for('main.contact'))

@main.route('/manufacturing')
def manufacturing():
    return render_template('manufacturing.html')

@main.route('/solar')
def solar():
    return render_template('solar.html')
