from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

#route to safety tips page
@app.route('/tips')
def tips():
    return render_template('tips.html')

#route to show the form
@app.route('/report')
def report():
    return render_template('report.html')

#route to process the form
@app.route('/submit_report', methods=['POST'])
def submit_report():
    location = request.form['location']
    report_type = request.form['type']
    description = request.form['description']

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO reports (location, type, description) VALUES (?, ?, ?)",
              (location, report_type, description))
    conn.commit()
    conn.close()

    return redirect('/report')