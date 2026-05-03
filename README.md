# 🚀 AI-Powered Resume Analyzer (Flask + Docker)

A modern **Flask-based web application** that analyzes resumes using a combination of **rule-based NLP + LLM-powered insights**.

Built with **Python, Flask, HTML/CSS**, and fully **Dockerized** for easy setup and deployment.

---

## 🔥 Features

* 🧠 **AI Resume Analysis**

  * Extracts skills, emails, phone numbers
  * Estimates experience (years)
  * Calculates job-match score

* 🤖 **LLM-Powered Suggestions**

  * Smart resume improvement tips
  * Bullet point rewrites with impact
  * One-line summary (strength + weakness)

* 📊 **Resume Scoring System**

  * Based on skills, experience, and relevance
  * Score out of 100

* 🌐 **Clean Web Interface**

  * Paste resume or upload `.txt`
  * Instant analysis results

* 🐳 **Docker Support**

  * Run anywhere with one command
  * No environment issues

---

## 🏗️ Tech Stack

* **Backend:** Python + Flask
* **Frontend:** HTML, CSS
* **AI Integration:** OpenAI API
* **Containerization:** Docker + Docker Compose

---

## 📁 Project Structure

```
flask-resume-docker/
│── app.py
│── analyzer.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── templates/
│   ├── index.html
│   └── analyze.html
│── static/
│   └── css/
│       └── style.css
```

---

## ⚙️ Setup & Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

---

### 2️⃣ Add Environment Variables (Optional for AI)

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

> ⚠️ If you don’t add this, the app will still work using basic (non-AI) analysis.

---

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

---

### 4️⃣ Open in Browser

* Resume Page → http://localhost:5000
* Analyzer → http://localhost:5000/analyze

---

## 🧪 Example Workflow

1. Paste your resume text
2. Click **Analyze**
3. Get:

   * ✅ Score (0–100)
   * 📌 Skills detected
   * 📈 Job match %
   * 💡 Suggestions
   * ✨ AI rewritten bullet points

---

## 🧠 How It Works

1. **Rule-Based Engine**

   * Regex for email, phone, years
   * Keyword matching for skills

2. **LLM Layer (Optional)**

   * Enhances suggestions
   * Generates rewritten bullet points
   * Provides structured JSON output

3. **Scoring System**

   * Skills → 50%
   * Experience → 20%
   * Job match → 20%
   * Contact info → 10%

---

## 🛠️ Customization

* Edit `SKILLS` in `analyzer.py` to match your target job
* Update `SAMPLE_JOB` for better job matching
* Modify UI in `templates/` and `static/css/`

---

## 🚀 Future Improvements

* 📄 PDF Resume Upload Support
* 📊 Resume History Dashboard
* 🔐 User Authentication
* ☁️ Deployment (AWS / Render / Railway)
* 🧠 Advanced LLM Resume Rewriting

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## ⭐ Support

If you like this project, consider giving it a **star ⭐** on GitHub!
