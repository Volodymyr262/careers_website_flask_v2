from sqlalchemy import create_engine, text
import os
from flask_login import LoginManager
from id_generate import uniqueid
import bcrypt
from flask import flash
db_key = os.environ["DB_CONNECTION"]

db_connection_string = db_key
engine = create_engine(db_connection_string, connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

#login_manager = LoginManager()
#login_manager.login_view = 'main.login'
#login_manager.init_app(app)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            jobs.append(dict(row))
    return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
            val = id
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return dict(rows[0])

def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("INSERT INTO applications(job_id, full_name,"
                     "email, linkedin_url, education, work_experience, "
                     "resume_url) VALUES (:job_id, :full_name, "
                     ":email, :linkedin_url, :education, :work_experience, "
                     ":resume_url)")
        conn.execute(query,
                     job_id=job_id, full_name=data['full_name'],
                     email=data['email'], linkedin_url=data['linkedin_url'],
                     education=data['education'],
                     work_experience=data['work_experience'],
                     resume_url=data['resume_url'])


def add_user(data):
    with engine.connect() as conn:
        unique_seq = uniqueid()
        user_id = next(unique_seq)
        encoded_password = data['password'].encode('utf-8')
        query = text("INSERT INTO user(id, full_name, email,"
                     "password) VALUES(:id, :full_name, :email, :password)")
        conn.execute(query,
                     id=user_id,
                     full_name=data['fullName'],
                     email=data['email'],
                     password=bcrypt.hashpw(encoded_password, bcrypt.gensalt()))


def login_check(data):
    with engine.connect() as conn:
        query = text("SELECT email, password FROM career.user WHERE email = :email")
        result = conn.execute(query, email=data['email'])
        results_as_dicts = []
        for row in result:
            result_dict = {
                'email': row['email'],
                'password': row['password']
            }
            results_as_dicts.append(result_dict)
        encoded_password = data['password'].encode('utf-8')
        encoded_password2 = results_as_dicts[0]['password'].encode('utf-8')
        if data['email'] == results_as_dicts[0]['email']:
            if bcrypt.checkpw(encoded_password, encoded_password2):
                return True
            else:
                flash('incorrect data', category='error')
                return False
        


