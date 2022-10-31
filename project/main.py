# main.py

import imaplib
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import mysql.connector
import os
import re
import ftplib
from flask_mail import Mail, Message
import imaplib
import email
import smtplib
from email.mime.text import MIMEText

HOSTNAME = "10.0.40.73"
USERNAME = "blueteam"
PASSWORD = "VTCCcyberTeam2022"

#set this up
ORG_EMAIL = "@sunpartners.local" 
FROM_EMAIL = "admin" + ORG_EMAIL 
FROM_PWD = "Blueteam2022" 
SMTP_SERVER = "10.0.40.73" 
SMTP_PORT = 25


REMOTE_SQL_IP = "10.0.40.76"
REMOTE_SQL_PORT = 3306
REMOTE_SQL_USER = "root"
REMOTE_SQL_PASS = "password"

main = Blueprint('main', __name__)

#get the flask app object

@main.route('/')
def index():
    #grab data from mySQL database named solar
    dbconfig = {
        'host': REMOTE_SQL_IP,
        'port': REMOTE_SQL_PORT,
        'user': REMOTE_SQL_USER,
        'password': REMOTE_SQL_PASS,
        'database': 'solar'
    }
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solar_arrays")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', rows=rows)

@main.route('/admin')
@login_required
def profile():
    if current_user.name == 'admin':
        mail = imaplib.IMAP4(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        emails = []
        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    #check if email_from is nonetype
                    if email_from is not None:
                        emails.append(msg)
        #get list of files
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.set_pasv(False)
        files = []
        allThings = ftp_server.nlst()
        for file in allThings:
            try:
                ftp_server.cwd(file)
                ftp_server.cwd('../')
            except:
                files += [file]
        ftp_server.quit()
        #get emails from smtp server

        return render_template('admin.html', name=current_user.name, files=files, emails=emails)

    else:
        return render_template('index.html')

#create download route
@main.route('/download/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    if current_user.name == 'admin':
        upload_folder = "uploads/"
        #empty the uploads folder
        try:
            for file in os.listdir(os.path.join(os.getcwd(), upload_folder)):
                os.remove(os.path.join(os.getcwd(), upload_folder, file))
        except:
            pass
        if re.search(r'(\.\.)|[/\\]', filename):
            flash('Invalid name')
            return redirect(url_for('main.admin'))
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        files = ftp_server.nlst()
        if filename in files:
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
            with open(os.path.join(upload_folder, filename), "wb") as file:
                ftp_server.retrbinary('RETR ' + filename, file.write)
            ftp_server.quit()
            return send_file(os.path.join(os.getcwd(), upload_folder, filename), as_attachment=True)
        else:
            ftp_server.quit()
            return redirect(url_for('main.profile'))
    else:
        return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/contact', methods=['POST'])
def contact_post():
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    #get all the form data from the contact form
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
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
        ftp_server.quit()
        #send mail
        msg = MIMEText('New file uploaded by ' + name + ' with email ' + email + ' and phone number ' + phone)
        msg['Subject'] = 'New contact form file uploaded from ' + name
        msg['From'] = FROM_EMAIL
        msg['To'] = FROM_EMAIL
        mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mailServer.login(FROM_EMAIL, FROM_PWD)
        mailServer.sendmail(FROM_EMAIL, [FROM_EMAIL], msg.as_string())
        return redirect(url_for('main.contact'))

@main.route('/manufacturing')
def manufacturing():
    return render_template('manufacturing.html')

@main.route('/solar')
def solar():
    return render_template('solar.html')
