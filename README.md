# Job Scraper & Cold Email Generator

A Streamlit web app that scrapes job postings from career pages, extracts required skills, and generates a personalized cold email to impress potential clients or recruiters.

## 🚀 Features

- **Scrape job postings** from any career page URL
- **Extract job details** (role, skills, description) using AI (LangChain + Groq)
- **Personalize your email**: Add a prompt about yourself (bio, achievements, experience)
- **Generate cold email**: AI writes a tailored email referencing your skills and experience


---
<br>
## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file:
   ```
   GROQ_API_TOKEN=your_groq_api_key_here
   ```

## 🏃‍♂️ Usage

```bash
streamlit run app.py
```

1. Enter the career/job posting URL.
2. (Optional) Edit your profile prompt to personalize your email.
3. Click **Scrape Job** to extract job details.
4. Click **Generate Email** to create a personalized cold email.
