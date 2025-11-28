from flask import Flask, render_template,request,url_for,flash,redirect
from analyzer import Analyzer_resume_text
import os

app =Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET","dev-secret")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("analyzer",methods=["POST","GET"])
def analyze():
    if request.method=="POST":
        resume_text=request.form.get("resume_text","").strip()
        uploaded = request.form.get("resume_file")
        if uploaded and uploaded.filename:
            filename = uploaded.filename.lower()
            if not filename.endswith(".txt"):
                flash("Only plain .txt files are accepted for upload (PDF support can be added).")
                return redirect(url_for("analyze"))
            try:
                content = uploaded.read().decode("utf-8",errors="ignore")
                resume_text = (resume_text + "\n\n" +content).strip() if resume_text else content
            except Exception as e:
                flash("There was an error reading the uploaded file.")
                return redirect(url_for("analyze"))
        
        if not resume_text:
            flash("Please provide resume text or upload a .txt file.")
            return redirect(url_for("analyze"))
        
        report = analyze_resume_text(resume_text)
        return render_template("analyze.html",report=report,resume_text=resume_text)
    else:
        return render_template("analyze.html",report=None,resume_text="")
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)