import os
import sys
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ CRITICAL: The 'google-genai' library is missing or failed to import!")
    sys.exit(1)

def run_agent():
    print("======= STARTING THE ULTIMATE IT CAREER SCOUT AGENT =======")
    
    # --- 1. HISTORY CACHE TRACKING ---
    history_file = "sent_courses.txt"
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = f.read().splitlines()
    else:
        history = []

    # --- 2. SECURITY ENVIRONMENT VERIFICATION ---
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    # --- 3. DUAL-TARGET MATRIX (ELITE UNIVERSITIES + TECH GIANTS) ---
    combined_targets = [
        # Elite University Tracks
        {"provider": "Harvard University (via edX/Coursera)", "keywords": ["CS50x: Introduction to Computer Science", "CS50P: Programming with Python"]},
        {"provider": "Stanford University (via Coursera)", "keywords": ["Introduction to Databases", "Machine Learning Specialization"]},
        {"provider": "University of Michigan (via Coursera)", "keywords": ["Python for Everybody", "Web Design for Everybody"]},
        
        # Tech Giant Absolute Free Tracks
        {"provider": "Cisco Networking Academy", "keywords": ["Introduction to Cybersecurity", "Networking Basics", "Python Essentials 1"]},
        {"provider": "Google Skillshop", "keywords": ["Google Analytics Certification", "Fundamentals of Digital Marketing"]},
        {"provider": "IBM Cognitive Class", "keywords": ["What is Data Science", "Python for Data Science", "Docker Essentials"]}
    ]
    
    scraped_courses = []
    for target in combined_targets:
        for keyword in target["keywords"]:
            if "Harvard" in target["provider"] or "Stanford" in target["provider"] or "Michigan" in target["provider"]:
                link = "https://www.coursera.org/"
            elif "Cisco" in target["provider"]:
                link = "https://skillsforall.com/"
            elif "Google" in target["provider"]:
                link = "https://skillshop.exceedlms.com/"
            else:
                link = "https://cognitiveclass.ai/"

            scraped_courses.append({
                "title": keyword,
                "provider": target["provider"],
                "link": link
            })

    new_courses = [c for c in scraped_courses if c["title"] not in history]
    
    if not new_courses:
        print("🔄 All courses have been seen. Resetting cache to refresh your options!")
        new_courses = scraped_courses
        if os.path.exists(history_file):
            os.remove(history_file)
    
    client = genai.Client(api_key=api_key)
    
    # --- 4. EXHAUSTIVE DEEP-DETAIL AI PROMPT ---
    prompt = f"""
    You are an expert IT Career Coach and Upwork Freelance Mentor. Your task is to write a highly detailed, comprehensive guide for each of the courses provided below. The reader is an 18-year-old beginner looking to scale a freelance business on Upwork from scratch.
    
    You must use simple, highly accessible language (avoid overly dense enterprise engineering jargon).
    You MUST output clean, valid HTML blocks (using <div>, <h3>, <h4>, <p>, <ul>, <ol>, and <li> tags). Do not use markdown backticks in your response.

    For EVERY single course, you must provide the following deep details:
    1. COURSE TITLE & PROVIDER: Wrap this in an <h3> tag. (If it is an elite school like Harvard or Stanford, style it or mention it prominently as a PRESTIGE TARGET!).
    2. OVERVIEW & WHAT YOU WILL LEARN: Explain exactly what skills this course teaches in everyday, practical terms.
    3. HOW TO JOIN (STEP-BY-STEP): Walk through the sign-up process.
    4. TOTAL DURATION & TIME COMMITMENT: Provide estimated total hours and a realistic schedule to finish it fast.
    5. THE 100% FREE CERTIFICATE/BADGE SYSTEM:
       - For Tech Giants (Cisco, Google, IBM): Explain the direct free badge/credential system (like Credly or Skillshop Profiles) and how to pass the final exam to claim it for $0.
       - For Universities (Harvard, Stanford, Michigan via Coursera/edX): Provide precise, step-by-step guidance on how to click the "Financial Aid Available" link right next to the Enroll button. Explain exactly how an 18-year-old student should answer the financial prompt honestly to get the paid verified certificate completely covered for 100% free.
    6. UPWORK FREELANCE & PORTFOLIO VALUE: Explain exactly how to phrase this credential on an Upwork bio or description. Tell them what specific beginner contracts this allows them to bid on.
    7. IT CAREER VALUE: Explain how this serves as a massive foundation for long-term corporate IT roles later down the road.
    8. DIRECT ACCESS LINK: Provide a beautifully formatted link using <a href="..." target="_blank">.

    Courses Data to process: {json.dumps(new_courses)}
    """
    
    # --- 5. SMART NETWORK RETRY LOOP & FALLBACK MODEL ENGINE ---
    models_to_try = ['gemini-2.5-flash', 'gemini-2.5-flash-lite']
    course_html_content = None
    
    for model_name in models_to_try:
        print(f"🛰️ Attempting content generation with model: {model_name}...")
        for attempt in range(1, 4):  # Try 3 times per model
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                course_html_content = response.text
                print(f"✅ Success! Content generated via {model_name}.")
                break  # Break out of the attempt loop if successful
            except Exception as e:
                error_str = str(e)
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    print(f"⚠️ Google Server Peak Load (503) on attempt {attempt}/3. Waiting to retry...")
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    print(f"🚨 Non-503 Error encountered: {error_str}")
                    break
        
        if course_html_content:
            break  # Break out of model loop if we have our data
            
    if not course_html_content:
        print("❌ CRITICAL: Google servers are completely slammed right now across all fallback channels. Stopping execution safely.")
        sys.exit(1)

    # --- 6. PREMIUM DARK MODE THEME HTML TEMPLATE ---
    html_email_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background-color: #121824; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; padding: 20px; margin: 0; }}
            .email-container {{ max-width: 750px; margin: 0 auto; background-color: #1e293b; border-radius: 16px; padding: 35px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
            .header {{ text-align: center; border-bottom: 3px solid #38bdf8; padding-bottom: 20px; margin-bottom: 30px; }}
            .header h1 {{ color: #38bdf8; font-size: 26px; margin: 0 0 10px 0; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }}
            .header p {{ color: #94a3b8; font-size: 15px; margin: 0; font-style: italic; }}
            h3 {{ color: #f59e0b; font-size: 20px; border-left: 5px solid #38bdf8; padding-left: 12px; margin-top: 35px; margin-bottom: 15px; font-weight: 700; }}
            h4 {{ color: #38bdf8; font-size: 15px; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }}
            p, li {{ color: #cbd5e1; line-height: 1.7; font-size: 15px; }}
            ul, ol {{ margin-top: 5px; padding-left: 20px; }}
            li {{ margin-bottom: 8px; }}
            a {{ color: #10b981; font-weight: bold; text-decoration: none; border-bottom: 1px dashed #10b981; }}
            a:hover {{ color: #34d399; border-bottom: 1px solid #34d399; }}
            .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #334155; color: #64748b; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>🎓 Full-Detail IT Certification Blueprint</h1>
                <p>Tech Giants & Elite Universities • 100% Free Certifications • Specialized for Upwork</p>
            </div>
            
            {course_html_content}
            
            <div class="footer">
                Generated securely by your GitHub Automation Agent.<br>
                Targeting zero-cost verified credentials for freelance business building.
            </div>
        </div>
    </body>
    </html>
    """

    # --- 7. SECURE GMAIL CONNECTION CONFIGURATION ---
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = 587
    sender_email = os.environ.get("SENDER_EMAIL")
    smtp_password = os.environ.get("SMTP_PASSWORD") or os.environ.get("EMAIL_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    if not all([sender_email, smtp_password, receiver_email]):
        print("❌ CRITICAL CONFIG ERROR: Missing email credentials inside GitHub Secrets.")
        sys.exit(1)
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "🚀 ULTIMATE Freelance Blueprint: Tech Giant & Ivy League Certifications"
        msg.attach(MIMEText(html_email_template, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📧 SUCCESS! Your ultra-detailed premium roadmap email has been sent.")
    except Exception as e:
        print(f"❌ SMTP TRANSMISSION FAILURE: {str(e)}")
        sys.exit(1)
    
    with open(history_file, "a") as f:
        for course in new_courses:
            f.write(course["title"] + "\n")

if __name__ == "__main__":
    run_agent()
