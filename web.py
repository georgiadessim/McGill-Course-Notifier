from flask import Flask, redirect, url_for, render_template, request
from VSBscrape import seatsavailability
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('notifier.html')

@app.route('/', methods=['POST'])
def my_form_post():
    term = request.form['term']
    subject = request.form['subject']
    course = request.form['course']
    receiver_email = request.form['email']
    print(term, subject, course, receiver_email)

    time_interval = 1  # Number of minutes between each scrape

    while True:
        seatsavailability(term, subject, course, receiver_email)
        time.sleep(time_interval * 60)

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')


if __name__ == "__main__":
    app.run()

