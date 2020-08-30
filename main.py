from flask import Flask, render_template, request, redirect, send_file
from programmers import get_jobs
from save import save_to_file

app = Flask("awesome job searching")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    lang = request.args.get('lang').lower()
    if len(lang) == 0:
        return redirect("/")

    existingJobs = db.get(lang)
    if existingJobs:
        jobs = existingJobs
    else:
        jobs = get_jobs(lang)
        db[lang] = jobs
    return render_template(
        "search.html", searchingBy=lang, job_len=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    lang = request.args.get('lang').lower()
    if not lang:
      raise Exception()
    jobs = db.get(lang)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect('/')

app.run(host="0.0.0.0")
