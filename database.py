from sqlalchemy import create_engine, text
import os

db_connection_string = "mysql+pymysql://5pqy8bybc1o3bqb691ez:pscale_pw_g0Eai7ErRcHKN1adkqxKaArZf29IvCv7VhllW1oiM26@aws.connect.psdb.cloud/career?charset=utf8mb4"
engine = create_engine(db_connection_string, connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            jobs.append(dict(row))
    return jobs