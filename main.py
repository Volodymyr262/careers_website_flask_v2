from flask import Flask, render_template, jsonify, request, redirect, flash, url_for, session
from database import load_jobs_from_db, load_job_from_db, \
    add_application_to_db, add_user, login_check


app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        if login_check(data):
            session['loggedin'] = True
            return redirect(url_for('heloo'))
        else:
            flash("Incorrect data", category='error')
    return render_template("login.html")


@app.route("/logout")
def logout():
    session['loggedin'] = False
    return redirect(url_for('login'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        if len(data['email']) < 4:
            flash("email must be greater than 4 characters", category='error')
        elif len(data['fullName']) < 2:
            flash("Full Name be greater than 2 characters", category='error')
        elif data['password'] != data['password1']:
            flash("Passwords don't match", category='error')
        elif len(data['password']) < 7:
            flash("Password is too short", category='error')
        else:
            add_user(data)
            return redirect(url_for('heloo'))
    return render_template("signup.html")


@app.route("/")
def heloo():
    JOBS = load_jobs_from_db()
    return render_template("home.html", jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
    JOBS = load_jobs_from_db()
    return jsonify(JOBS)


@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Found", 404
    else:
        return render_template('jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
    data = request.form
    job =load_job_from_db(id)
    add_application_to_db(job_id=id, data=data)
    return render_template("applicatin_submitted.html",
                           application=data, job=job)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host ='0.0.0.0', debug=True)