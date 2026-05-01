<div align="center">

# 🤖 Multi-Agent-With-Crewai

### AI-Powered Corporate Training Analysis Platform

**An intelligent multi-agent system that analyzes companies, identifies skill gaps, and recommends personalized training courses using advanced AI.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-1.14%2B-FF6B35?logoColor=white)](https://docs.crewai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Janaelpardisi/Multi-Agent-With-Crewai?style=social)](https://github.com/Janaelpardisi/Multi-Agent-With-Crewai)

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [How It Works](#-how-it-works) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration--customization)
- [Troubleshooting](#-troubleshooting)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Multi-Agent-With-Crewai** is an enterprise-grade AI system that leverages multiple specialized AI agents to perform comprehensive company analysis and training recommendations. 

It uses **CrewAI's multi-agent orchestration** to:
- 🔍 Analyze company job requirements
- 📊 Identify critical skill gaps
- 🎓 Find the best training courses
- 📄 Generate professional reports

Perfect for **HR teams, talent development departments**, and **corporate training managers** who need data-driven insights for employee development.

---

## 🌟 Features

### 🏢 **Company Analysis Agent**
- Searches LinkedIn and job boards for company postings
- Extracts detailed job requirements and responsibilities
- Identifies required skills (technical & soft skills)
- Provides company industry context and summary

### 🔎 **Skills Gap Detector Agent**
- Analyzes extracted skills from job postings
- Prioritizes skills by importance and frequency
- Evaluates market demand and business impact
- Generates intelligent search queries for course discovery

### 📚 **Course Finder Agent**
- Searches Coursera and Udemy platforms
- AI-powered web scraping with ratings and reviews
- Ranks courses by relevance, price, and quality
- Filters by industry-specific relevance

### 📊 **Training Report Author Agent**
- Compiles all findings into structured data
- Generates professional HTML reports
- Creates actionable training recommendations
- Produces executive-ready documentation

### ⚡ **Additional Capabilities**
- **Real-time Progress Tracking** — Live streaming updates as agents work
- **RESTful API** — Clean, intuitive endpoints
- **Responsive UI** — Modern web interface
- **JSON Output** — Machine-readable results
- **Async Processing** — Non-blocking analysis jobs

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Multi-Agent Framework** | CrewAI | Orchestrate and coordinate AI agents |
| **Web Framework** | FastAPI | High-performance REST API |
| **LLM** | OpenAI GPT-4 | Agent reasoning & analysis |
| **Web Search** | Tavily API | Real-time job market data |
| **Web Scraping** | ScrapeGraphAI | Intelligent course extraction |
| **Data Validation** | Pydantic | Structured output validation |
| **Web Server** | Uvicorn | ASGI server |
| **Frontend** | HTML5/CSS3/JS | Interactive user interface |

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Python 3.10** or higher
- **pip** package manager
- API Keys from:
  - 🔑 [OpenAI](https://platform.openai.com/) — `OPENAI_API_KEY`
  - 🔑 [Tavily](https://tavily.com/) — `TAVILY_API_KEY`
  - 🔑 [ScrapeGraphAI](https://scrape-graph-ai.com/) — `SGAI_API_KEY`
  - 🔑 [AgentOps](https://agentops.ai/) — `AGENTOPS_API_KEY` (optional)

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Janaelpardisi/Multi-Agent-With-Crewai.git
cd Multi-Agent-With-Crewai
```

#### 2️⃣ Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here

# ScrapeGraphAI
SGAI_API_KEY=your_scrapegraphai_api_key_here

# AgentOps (Optional - for agent monitoring)
AGENTOPS_API_KEY=your_agentops_api_key_here
```

#### 5️⃣ Run the Application

**Option A: Using Batch File (Windows)**
```bash
run.bat
```

**Option B: Using Python**
```bash
python main.py
```

**Option C: Using Uvicorn Directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ The server will be available at: **http://localhost:8000**

---

## 📋 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze` | Start company analysis |
| `GET` | `/api/analyze/{job_id}` | Get job status & results |
| `GET` | `/api/analyze/stream/{job_id}` | Stream live updates |
| `GET` | `/` | Access web UI |

---

### 1. POST `/api/analyze` — Start Analysis

**Submit a company for analysis**

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "TechCorp Inc",
    "industry": "Software Development",
    "min_job_posts": 2,
    "top_skills_no": 5,
    "top_courses_no": 3,
    "top_platforms_no": 2
  }'
```

**Request Body Schema:**
```json
{
  "company_name": "string (required)",
  "industry": "string (required)",
  "min_job_posts": "integer (default: 1)",
  "top_skills_no": "integer (default: 2)",
  "top_courses_no": "integer (default: 2)",
  "top_platforms_no": "integer (default: 2)"
}
```

**Response (201 Created):**
```json
{
  "job_id": "484dc247-6b92-4eb6-b048-7bfd105de696",
  "status": "running",
  "message": "Analysis started. Check /api/analyze/{job_id} for status"
}
```

---

### 2. GET `/api/analyze/{job_id}` — Get Status & Results

**Retrieve analysis results**

**Request:**
```bash
curl http://localhost:8000/api/analyze/484dc247-6b92-4eb6-b048-7bfd105de696
```

**Response (200 OK):**
```json
{
  "job_id": "484dc247-6b92-4eb6-b048-7bfd105de696",
  "status": "completed",
  "progress": 100,
  "message": "Analysis completed successfully",
  "results": {
    "company_analysis": {
      "company_name": "TechCorp Inc",
      "industry": "Software Development",
      "company_summary": "TechCorp is a leading software company...",
      "job_posts": [
        {
          "job_title": "Senior Full Stack Engineer",
          "required_skills": ["Python", "React", "PostgreSQL"],
          "experience_level": "Senior",
          "source_url": "https://linkedin.com/..."
        }
      ],
      "top_required_skills": ["Python", "React", "PostgreSQL"]
    },
    "skills_gap": {
      "total_skills_found": 15,
      "priority_skills_for_training": [
        {
          "skill_name": "Python",
          "importance_level": "High",
          "reason": "Required in 80% of job postings",
          "suggested_search_queries": ["Advanced Python Development"]
        }
      ]
    },
    "courses": {
      "total_courses_found": 12,
      "courses": [
        {
          "skill_name": "Python",
          "course_title": "Complete Python Bootcamp",
          "platform": "Udemy",
          "course_url": "https://udemy.com/...",
          "price": "$15.99",
          "duration": "25 hours",
          "rating": 4.8,
          "level": "Intermediate"
        }
      ]
    },
    "report_url": "/outputs/484dc247-6b92-4eb6-b048-7bfd105de696/step_4_report.html"
  }
}
```

**Status Values:**
- `running` — Analysis in progress
- `completed` — Analysis finished successfully
- `failed` — Analysis encountered an error

---

### 3. GET `/api/analyze/stream/{job_id}` — Stream Live Updates

**Get real-time progress updates**

**Request:**
```bash
curl http://localhost:8000/api/analyze/stream/484dc247-6b92-4eb6-b048-7bfd105de696
```

**Response (Server-Sent Events):**
```
data: {"type":"message","content":"Analyzing company...","agent":"Company Analyzer Agent"}
data: {"type":"progress","value":25}
data: {"type":"message","content":"Identifying skill gaps...","agent":"Skills Gap Detector"}
data: {"type":"progress","value":50}
...
```

---

## 📁 Project Structure

```
Multi-Agent-With-Crewai/
│
├── 📄 main.py                      # FastAPI application & API endpoints
├── 📄 crew_logic.py                # CrewAI agents and task definitions
├── 📄 requirements.txt             # Python dependencies
├── 📄 run.bat                      # Windows startup script
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # This file
│
├── 📁 static/                      # Frontend assets
│   └── index.html                  # Web UI interface
│
└── 📁 outputs/                     # Analysis results (auto-created)
    └── {job_id}/                   # Per-job output directory
        ├── step_1_company.json     # Company analysis results
        ├── step_2_skills_gap.json  # Skills gap analysis
        ├── step_3_courses.json     # Course recommendations
        └── step_4_report.html      # Final HTML report
```

---

## 🤖 How It Works

### Agent Pipeline Architecture

The system uses a sequential pipeline of specialized agents:

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT: Company Info                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  🏢 Company Analyzer Agent     │
        │  ─────────────────────────────  │
        │  • Search job postings         │
        │  • Extract company info        │
        │  • List required skills        │
        │  OUTPUT: step_1_company.json   │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  🔍 Skills Gap Detector        │
        │  ─────────────────────────────  │
        │  • Analyze skill frequency     │
        │  • Prioritize by importance    │
        │  • Generate search queries     │
        │  OUTPUT: step_2_skills_gap.json│
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  📚 Course Finder Agent        │
        │  ─────────────────────────────  │
        │  • Search platforms            │
        │  • Scrape course details       │
        │  • Rank by relevance           │
        │  OUTPUT: step_3_courses.json   │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  📊 Report Author Agent        │
        │  ─────────────────────────────  │
        │  • Compile all findings        │
        │  • Generate HTML report        │
        │  • Format recommendations      │
        │  OUTPUT: step_4_report.html    │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │    Final Training Report       │
        │    Ready for stakeholders      │
        └────────────────────────────────┘
```

### Agent Descriptions

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Company Analyzer** | Research Specialist | Finds and analyzes job postings, extracts skill requirements |
| **Skills Gap Detector** | Data Analyst | Identifies patterns, prioritizes critical skills |
| **Course Finder** | Research Specialist | Discovers and evaluates training courses |
| **Report Author** | Technical Writer | Compiles findings into professional documentation |

---

## 🔧 Configuration & Customization

### Adjust Analysis Parameters

Edit `main.py` to change default parameters:

```python
class AnalysisRequest(BaseModel):
    company_name: str
    industry: str
    min_job_posts: int = 1          # Increase for more job posts
    top_skills_no: int = 2          # Number of skills to analyze
    top_courses_no: int = 2         # Courses per skill
    top_platforms_no: int = 2       # Platforms to search
```

### Customize Agent Behavior

Edit `crew_logic.py` to modify:

```python
# Change LLM model
basic_llm = LLM(model="gpt-4", temperature=0.3)

# Modify agent goals
agent = Agent(
    role="...",
    goal="Your custom goal here",
    backstory="...",
)

# Adjust task descriptions
task = Task(
    description="Custom task description",
    expected_output="Your expected output format"
)
```

### Environment Variables

```env
# Model Configuration
OPENAI_API_KEY=...              # GPT-4 access
OPENAI_MODEL=gpt-4              # Change LLM model

# Search & Scraping
TAVILY_API_KEY=...              # Web search
SGAI_API_KEY=...                # Web scraping

# Monitoring
AGENTOPS_API_KEY=...            # Agent monitoring
```

---

## 🐛 Troubleshooting

### ❌ "API Key not found" Error

**Solution:**
- Verify `.env` file exists in project root
- Check all required keys are present and valid
- Restart the server after updating `.env`

```bash
# Verify .env exists
ls -la .env

# Check key format
cat .env
```

### ❌ "ModuleNotFoundError" Error

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify virtual environment is activated
which python  # Linux/Mac
where python  # Windows
```

### ❌ Slow Analysis / Timeouts

**Solution:**
- Reduce `min_job_posts` parameter (fewer job posts = faster analysis)
- Reduce `top_courses_no` parameter
- Check API rate limits on OpenAI and Tavily dashboards
- Consider waiting time: analysis can take 2-5 minutes depending on settings

### ❌ Course Scraping Fails

**Solution:**
- Verify `SGAI_API_KEY` is active
- Some websites block scrapers (try different platforms)
- Check Tavily API quota
- Reduce `top_platforms_no` to 1

### ❌ Port 8000 Already in Use

**Solution:**
```bash
# Use different port
uvicorn main:app --port 8001

# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## 📝 Examples

### Example 1: Analyze Tech Startup

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "OpenAI",
    "industry": "Artificial Intelligence",
    "min_job_posts": 3,
    "top_skills_no": 5,
    "top_courses_no": 3,
    "top_platforms_no": 2
  }'
```

**Expected Output:**
- Company profile and mission
- Top 5 skills (Python, Machine Learning, etc.)
- 3-5 recommended courses per skill
- Professional HTML report

### Example 2: Python Script

```python
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

# Submit analysis request
response = requests.post(f"{BASE_URL}/api/analyze", json={
    "company_name": "Netflix",
    "industry": "Streaming & Media",
    "min_job_posts": 2,
    "top_skills_no": 3,
    "top_courses_no": 2,
    "top_platforms_no": 2
})

job_data = response.json()
job_id = job_data["job_id"]
print(f"✅ Analysis started: {job_id}")

# Poll for results
while True:
    status_response = requests.get(f"{BASE_URL}/api/analyze/{job_id}")
    status = status_response.json()
    
    print(f"Status: {status['status']} | Progress: {status['progress']}%")
    
    if status['status'] == 'completed':
        results = status['results']
        print("\n📊 Analysis Complete!")
        print(json.dumps(results, indent=2))
        break
    elif status['status'] == 'failed':
        print("❌ Analysis failed")
        break
    
    sleep(5)  # Check every 5 seconds
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- 🐛 **Report Bugs** — Open an issue with details
- 💡 **Suggest Features** — Share your ideas
- 🔧 **Submit Pull Requests** — Improve the code
- 📚 **Improve Docs** — Help others understand

### Steps to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You're free to use this project for:
- ✅ Personal projects
- ✅ Commercial applications
- ✅ Educational purposes
- ✅ Modifications and distributions

---

## 🙏 Acknowledgments

- **CrewAI** — For the amazing multi-agent framework
- **FastAPI** — For the high-performance web framework
- **OpenAI** — For GPT-4 API
- **Tavily** — For web search capabilities
- **ScrapeGraphAI** — For intelligent web scraping

---

## 📧 Contact & Support

- 👤 **Author**: Jana Ashraf
- 📧 **Email**: [contact info]
- 🐙 **GitHub**: [@Janaelpardisi](https://github.com/Janaelpardisi)
- 💬 **Issues**: [GitHub Issues](https://github.com/Janaelpardisi/Multi-Agent-With-Crewai/issues)

---

<div align="center">

### ⭐ If you found this useful, please consider giving it a star!

**Built with ❤️ by Jana Ashraf**

</div>
#
