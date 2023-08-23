from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
    'id':1,
    'title': 'Data Analyst',
    'location':'Bengaluru, India',
    'salary': 'Rs. 1,00,000'
},
{
    'id':2,
    'title': 'Scientist',
    'location':'Dehli, India',
    'salary': 'Rs. 15,00,000'
},
{
    'id':3,
    'title': 'Backend Engineer',
    'location':'Remote',
    'salary': '$ 40000'
},
{
    'id':4,
    'title': 'Frontend Engineer',
    'location':'San Francisko USA',
}
]

@app.route("/")
def heloo():
    return render_template("home.html", jobs=JOBS,
                           company_name="Jovian")

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', debug=True)