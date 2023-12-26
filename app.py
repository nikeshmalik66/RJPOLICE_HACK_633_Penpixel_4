#Importing Libraries
from main import generate
from flask import Flask, request, jsonify, render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import os
from PIL import Image
import pytesseract
import csv
import pandas as pd
import re

app = Flask(__name__)

# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crime_reports.db'  
db = SQLAlchemy(app)

class CrimeReport(db.Model):
    firNo = db.Column(db.String, primary_key=True)
    district = db.Column(db.String)
    date = db.Column(db.Date)
    day = db.Column(db.String)
    dateOfOccurrence = db.Column(db.Date)
    placeOfOccurrence = db.Column(db.String)
    name = db.Column(db.String)
    dob = db.Column(db.Date)
    nationality = db.Column(db.String)
    occupation = db.Column(db.String)
    address = db.Column(db.String)
    reportedCrime = db.Column(db.String)
    propertiesInvolved = db.Column(db.String)
    modelOutput = db.Column(db.String)

# Create the database tables
# @app.before_first_request
# def create_tables():
#     db.create_all()

# app routes and api endpoints

# for index
@app.route("/")
def index():
    return render_template("index.html")

#for crime reporting page
@app.route("/report-crime")
def reportCrime():
    return render_template("report-crime.html")

# App route for processing the reported crime
@app.route('/process_reported_crime', methods=['POST'])
def process_reported_crime():
                            
    data = request.json
    reported_crime = data.get('reportedCrime')          # Extract the reportedCrime data from the POST request
    ipc_sections= generate(reported_crime)              # Using the generate function from main.py to process the reported crime
    return jsonify({'result': ipc_sections})

@app.route('/ipc-dataset')
def ipcDataset():

    csv_file_path = 'static/resources/ipc_ds.csv'
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Assuming the first row contains column headers
            data = list(csv_reader)
    except FileNotFoundError:
        return "CSV file not found."

    return render_template('ipc-dataset.html', headers=headers, data=data)

# App route for OCR crime reporting page
@app.route("/ocr-analysis")
def ocrCrimeAnalysis():
    return render_template("ocr-recognition.html")

# Initialize the tesseract reader
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    file_type = request.form['fileType']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file_type == 'image':
        # Save the file temporarily
        temp_path = os.path.join('uploads', file.filename)
        file.save(temp_path)

        # Perform OCR on the image
        image = Image.open(temp_path)
        extracted_text = pytesseract.image_to_string(image, lang='hin+eng')

        # os.remove(temp_path) # Optionally, delete the temporary file

        generated_output = generate(extracted_text)
        return jsonify({"message": extracted_text, "generated_output": generated_output})

    # Add logic for PDF 

    return jsonify({"message": "File uploaded but not processed"})

# api endpoint for storing form details into the database
@app.route('/submit_report', methods=['POST'])
def submit_report():
    data = request.json
    if CrimeReport.query.get(data['firNo']):
        return jsonify({'error': 'FIR No already exists'}), 409  

    report = CrimeReport(**data)
    db.session.add(report)
    db.session.commit()
    return jsonify({'success': 'Report submitted successfully'}), 200

# App route for OCR crime reporting page
@app.route("/fir-form")
def firForm():
    return render_template("fir-form.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database table
    app.run(debug=True)
