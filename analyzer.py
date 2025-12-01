
import re
import os
import json
from collections import Counter


SKILLS = [
    "python", "flask", "django", "sqlalchemy", "postgresql", "mysql", "docker",
    "docker-compose", "git", "rest", "api", "aws", "gcp", "azure", "linux",
    "html", "css", "javascript", "react", "node", "pandas", "numpy", "celery",
    "redis", "mongodb", "sql", "unit test", "pytest", "ci/cd", "github actions",
]

SAMPLE_JOB = [
    "python", "flask", "docker", "rest api", "postgresql", "sqlalchemy", "aws", "git"
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9.\-_+]+@[a-zA-Z0-9\-_]+\.[a-zA-Z0-9.\-_]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s-]?)?(\d{10}|\d{5}[\s-]\d{5}|\d{3}[\s-]\d{3}[\s-]\d{4})")
YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
YEARS_OF_EXP_RE = re.compile(r"(\d+)\s+(?:years|yrs|year)")


def normalize_text(text):
    return text.lower()

def extract_emails(text):
    return list(set(EMAIL_RE.findall(text)))

def extract_phones(text):
    phones = PHONE_RE.findall(text)
    results = []
    for g in phones:
        joined = "".join(g)
        s = re.sub(r"\s+|-", "", joined)
        if len(s) >= 7:
            results.append(s)
    return list(set(results))

def extract_skills(text, skills=SKILLS):
    txt = normalize_text(text)
    found = []
    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, txt):
            found.append(skill)
    return sorted(found, key=lambda x: -len(x))

def estimate_experience_years(text):
    txt = text.lower()
    m = YEARS_OF_EXP_RE.search(txt)
    if m:
        try:
            return int(m.group(1))
        except:
            pass
    four_digit_years = [int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]
    if four_digit_years:
        span = max(four_digit_years) - min(four_digit_years)
        return span if span > 0 else 1
    return 0

def keyword_overlap_score(resume_text, job_keywords=SAMPLE_JOB):
    txt = normalize_text(resume_text)
    cnt = 0
    for kw in job_keywords:
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", txt):
            cnt += 1
    return cnt / max(1, len(job_keywords))

def missing_sections_suggestions(text):
    suggestions = []
    txt = text.lower()
    if "education" not in txt and "degree" not in txt:
        suggestions.append("Add an Education section (degrees, institutions, graduation years).")
    if "project" not in txt and "projects" not in txt:
        suggestions.append("Add a Projects section with 1–3 bullet points each (tech used + impact).")
    if "experience" not in txt and "work" not in txt:
        suggestions.append("Add an Experience or Work History section with company, role, dates, and impact.")
    return suggestions

def actionable_suggestions_local(report):
    sug = []
    if not (report.get("emails") or report.get("phones")):
        sug.append("Add contact information (email and/or phone) near the top.")
    if report.get("experience_years", 0) == 0:
        sug.append("Clarify your work dates or total years of experience (e.g., '3 years experience').")
    missing = [s for s in ["python", "flask", "docker"] if s not in [x.lower() for x in report.get("skills_found", [])]]
    if missing:
        sug.append(f"Consider explicitly listing key skills: {', '.join(missing)} (if you have them).")
    if "improv" not in report.get("resume_text", "").lower() and "improve" not in report.get("resume_text", "").lower():
        sug.append("Use metrics in bullet points (e.g., 'Reduced load time by 30%').")
    if report.get("job_match_score", 0) < 0.4:
        sug.append("Tailor the resume to the job: include keywords from the job description and highlight relevant projects.")
    return sug


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini") 

def call_llm_for_suggestions(report):

    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        openai.api_key = OPENAI_API_KEY
    except Exception as e:
        return None

    prompt = build_prompt_for_llm(report)

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides concise, actionable resume suggestions and rewrites in JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.2,
        )
        text = response["choices"][0]["message"]["content"].strip()    
        parsed = try_parse_json_from_text(text)
        if parsed:
            return parsed
    
        return {"suggestions": [text]}
    except Exception as e:
        return None

def build_prompt_for_llm(report):
    """
    Build a careful prompt asking the model to return JSON:
    { "suggestions": [...], "rewrites": [...] }
    rewrites are optional; suggestions should be short, actionable items.
    """
    resume_excerpt = (report.get("resume_text") or "")[:3000]  
    skills = ", ".join(report.get("skills_found", [])) or "None detected"
    emails = ", ".join(report.get("emails", [])) or "None"
    phones = ", ".join(report.get("phones", [])) or "None"
    experience = report.get("experience_years", 0)
    job_match = round(report.get("job_match_score", 0) * 100)
    prompt = f"""
You will return a JSON object only. Do not add extra commentary.

Context:
Resume excerpt (first 3000 chars): \"\"\"{resume_excerpt}\"\"\"
Detected emails: {emails}
Detected phones: {phones}
Detected skills: {skills}
Estimated years of experience: {experience}
Job match percentage (approx): {job_match}%

Task:
1) Provide an array `suggestions` with up to 6 short, actionable items to improve the resume (one sentence each).
2) Provide an array `rewrites` containing up to 5 improved bullet points based on the resume excerpt. Each rewrite should be a single short sentence demonstrating strong impact, including numbers/metrics if possible — if the resume excerpt lacks metrics, produce suggested metrics in brackets like [e.g., reduced X by 20%] so the user can replace with real numbers.
3) Provide a short `summary` sentence (one line) that captures the main strengths and one weakness to fix.
Return strictly valid JSON, for example:
{{"suggestions": ["...","..."], "rewrites": ["..."], "summary": "..." }}
"""
    return prompt

def try_parse_json_from_text(text):
    """
    Attempt to find and parse JSON inside the model's text output.
    """

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except:
            pass
    try:
        return json.loads(text)
    except:
        return None

def compute_score(report):
    skills_score = min(1.0, len(report.get("skills_found", [])) / max(1, len(SKILLS)))
    contact_score = 1.0 if (report.get("emails") or report.get("phones")) else 0.0
    exp_score = min(1.0, report.get("experience_years", 0) / 5.0)
    job_score = report.get("job_match_score", 0)
    total = (skills_score * 0.5 + contact_score * 0.1 + exp_score * 0.2 + job_score * 0.2)
    return round(total * 100)

def analyze_resume_text(text):
    if not text or not text.strip():
        return {"error": "Empty resume text provided."}
    resume_text = text
    emails = extract_emails(text)
    phones = extract_phones(text)
    skills_found = extract_skills(text)
    experience_years = estimate_experience_years(text)
    job_match = keyword_overlap_score(text)

    report = {
        "resume_text": resume_text,
        "emails": emails,
        "phones": phones,
        "skills_found": skills_found,
        "experience_years": experience_years,
        "job_match_score": round(job_match, 2),
    }
    report["missing_sections"] = missing_sections_suggestions(text)
    # First compute quick local suggestions
    local_suggestions = actionable_suggestions_local(report)
    # Now try LLM to get richer suggestions & rewrites (if configured)
    llm_result = call_llm_for_suggestions({
        "resume_text": resume_text,
        "emails": emails,
        "phones": phones,
        "skills_found": skills_found,
        "experience_years": experience_years,
        "job_match_score": job_match,
    })
    if llm_result:
        # Prefer LLM suggestions if available
        report["suggestions"] = llm_result.get("suggestions", local_suggestions)
        report["rewrites"] = llm_result.get("rewrites", [])
        report["summary"] = llm_result.get("summary", "")
    else:
        report["suggestions"] = local_suggestions
        report["rewrites"] = []
        report["summary"] = ""

    report["score"] = compute_score(report)
    report["top_skills"] = report["skills_found"][:10]
    return report
