from flask import render_template, flash, redirect, request, session, url_for, jsonify
from app import app, db, models

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/parli', methods=['GET'])
def parli():
    return render_template("parli.html")

@app.route('/tournaments', methods=['GET'])
def tournaments():
    return render_template("tournament.html")

@app.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template("contact_us.html")

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template("about_us.html")

@app.route('/join_us', methods=['GET'])
def join_us():
    return render_template("join_us.html")

@app.route('/faqs', methods=['GET'])
def faqs():
    return render_template("faq.html")

@app.route('/rules_and_guides', methods=['GET'])
def rules_and_guides():
    return redirect('http://apdaweb.org/guide/rules')
