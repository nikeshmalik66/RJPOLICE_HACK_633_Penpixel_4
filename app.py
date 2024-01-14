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
from datetime import datetime
from flask import send_file, make_response
import io
import pdfkit 

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
    data = request.get_json()
    
    reported_crime = data.get('reportedCrime')          # Extract the reportedCrime data from the POST request
    ipc_sections= generate(reported_crime)               # Using the generate function from main.py to process the reported crime

    # Extract data from form fields
    fir_no = data.get('firNo') 
    district = data.get('district')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    day = data.get('day')
    date_of_occurrence = datetime.strptime(data.get('dateOfOccurrence'), '%Y-%m-%d')
    place_of_occurrence = data.get('placeOfOccurrence')
    name = data.get('name')
    dob = datetime.strptime(data.get('dob'), '%Y-%m-%d')
    nationality = data.get('nationality')
    occupation = data.get('occupation')
    address = data.get('address')
    reported_crime = data.get('reportedCrime')
    properties_involved = data.get('propertiesInvolved')
    model_output = data.get('modelOutput')

    # Create a new CrimeReport instance with the form data
    new_report = CrimeReport(
        firNo=fir_no,
        district=district,
        date=date,
        day=day,
        dateOfOccurrence=date_of_occurrence,
        placeOfOccurrence=place_of_occurrence,
        name=name,
        dob=dob,
        nationality=nationality,
        occupation=occupation,
        address=address,
        reportedCrime=reported_crime,
        propertiesInvolved=properties_involved,
        modelOutput=model_output
    )

    # Add the new report to the database session and commit
    db.session.add(new_report)
    db.session.commit()

    # Redirect to a confirmation page or flash a success message
    # flash('Crime report submitted successfully!')                       
                            
          
    return jsonify({'result': ipc_sections})

# Api endpoint for submitting selected ipc sections 
@app.route('/submit_ipc_sections', methods=['POST'])
def submit_ipc_sections():
    data = request.get_json()
    fir_no = data.get('firNo')
    ipc_sections = data.get('ipcSections')

    # Fetch the report using the FIR number
    report = CrimeReport.query.filter_by(firNo=fir_no).first()
    if report:
        # Update the report with the selected IPC sections
        report.modelOutput = ipc_sections
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'IPC sections updated successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Report not found'}), 404
    
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
# @app.route('/submit_crime_report', methods=['POST'])
# def submit_crime_report():
#     if request.method == 'POST':
#         # Extract data from form fields
#         fir_no = request.form['firNo']
#         district = request.form['district']
#         date = datetime.strptime(request.form['date'], '%Y-%m-%d')
#         day = request.form['day']
#         date_of_occurrence = datetime.strptime(request.form['dateOfOccurrence'], '%Y-%m-%d')
#         place_of_occurrence = request.form['placeOfOccurrence']
#         name = request.form['name']
#         dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
#         nationality = request.form['nationality']
#         occupation = request.form['occupation']
#         address = request.form['address']
#         reported_crime = request.form['reportedCrime']
#         properties_involved = request.form['propertiesInvolved']
#            = request.form['modelOutput']

#         # Create a new CrimeReport instance with the form data
#         new_report = CrimeReport(
#             firNo=fir_no,
#             district=district,
#             date=date,
#             day=day,
#             dateOfOccurrence=date_of_occurrence,
#             placeOfOccurrence=place_of_occurrence,
#             name=name,
#             dob=dob,
#             nationality=nationality,
#             occupation=occupation,
#             address=address,
#             reportedCrime=reported_crime,
#             propertiesInvolved=properties_involved,
#             modelOutput=model_output
#         )

#         # Add the new report to the database session and commit
#         db.session.add(new_report)
#         db.session.commit()

#         # Redirect to a confirmation page or flash a success message
#         flash('Crime report submitted successfully!')
#         return redirect(url_for('report_crime_form'))  # Redirect to the index or another appropriate page

#     return redirect(url_for('report_crime_form'))
# App route for OCR crime reporting page
@app.route("/fir-form")
def firForm():
    return render_template("fir-form.html")

# App route for displating fir report
@app.route('/display_fir/<fir_no>')
def display_fir(fir_no):
    # Fetch the FIR report using the FIR number
    report = CrimeReport.query.filter_by(firNo=fir_no).first()

    if report:
        # Render a template with the report details
        return render_template('display-report.html', report=report)
    else:
        return 'Report not found', 404


# Configure the path to the wkhtmltopdf executable
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/download_fir_pdf/<fir_no>')
def download_fir_pdf(fir_no):
    # Fetch the FIR report using the FIR number
    report = CrimeReport.query.filter_by(firNo=fir_no).first()

    if report:
        # Prepare HTML content for PDF generation
        rendered_html = render_template('display-report.html', report=report)

        # Convert the HTML to PDF
        pdf_content = pdfkit.from_string(rendered_html, False, options={"enable-local-file-access": ""}, configuration=config)

        # Create an in-memory file
        pdf_file = io.BytesIO(pdf_content)

        # Create a response object and set the correct headers
        response = make_response(pdf_file.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=FIR_Report_{fir_no}.pdf'

        return response
    else:
        return 'Report not found', 404



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database table
    app.run(debug=True)
