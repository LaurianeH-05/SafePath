from flask import Flask, render_template

app = Flask(__name__)

@app.route('/tips')
def tips():
    return render_template('tips.html')