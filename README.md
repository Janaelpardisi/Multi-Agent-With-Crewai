# Multi Agent With Crewai Framework

An AI-powered multi-agent system that analyzes companies, identifies skill gaps, and recommends personalized training courses. Built with **CrewAI**, **FastAPI**, and powered by **OpenAI GPT-4**.

---

## 🌟 Features

- **Company Analysis Agent** — Extracts job requirements and skills from company job postings via LinkedIn and job boards
- **Skills Gap Detector** — Identifies the most critical skill gaps based on market demand and business impact
- **Course Finder Agent** — Discovers and ranks the best training courses from Coursera and Udemy
- **Training Report Generator** — Creates professional HTML reports with actionable training recommendations
- **Real-time Progress Tracking** — Stream live updates as agents complete their analysis
- **RESTful API** — Simple, fast API endpoints for seamless integration
- **Modern UI** — Responsive web interface with real-time job status monitoring

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- API Keys:
  - `OPENAI_API_KEY` — From OpenAI
  - `TAVILY_API_KEY` — For web search capabilities
  - `SGAI_API_KEY` — For web scraping (ScrapeGraphAI)
  - `AGENTOPS_API_KEY` — Optional, for agent monitoring

### Installation

1. **Clone or navigate to the project directory**

```bash
cd "Multi Agent With Crewai Framework"
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
SGAI_API_KEY=your_scrapegraphai_api_key
AGENTOPS_API_KEY=your_agentops_api_key
```

### Running the Application

**Using the batch file (Windows):**

```bash
run.bat
```

**Or manually with Python:**

```bash
python main.py
```

The server will start at `http://localhost:8000`

---

## 📋 API Documentation

### Endpoint: `/api/analyze`

**Method:** `POST`

**Description:** Submits a company for skill gap analysis

**Request Body:**

```json
{
  "company_name": "TechCorp Inc",
  "industry": "Software Development",
  "min_job_posts": 1,
  "top_skills_no": 2,
  "top_courses_no": 2,
  "top_platforms_no": 2
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `company_name` | string | *required* | Name of the company to analyze |
| `industry` | string | *required* | Industry/sector (e.g., "Tech", "Finance") |
| `min_job_posts` | integer | 1 | Number of job posts to analyze |
| `top_skills_no` | integer | 2 | Number of top skills to identify |
| `top_courses_no` | integer | 2 | Number of courses per skill |
| `top_platforms_no` | integer | 2 | Number of platforms to search |

**Response:**

```json
{
  "job_id": "484dc247-6b92-4eb6-b048-7bfd105de696",
  "status": "success",
  "message": "Analysis completed successfully"
}
```

### Endpoint: `/api/analyze/{job_id}`

**Method:** `GET`

**Description:** Retrieves the status and results of an analysis job

**Response:**

```json
{
  "status": "completed",
  "progress": 100,
  "results": {
    "company_analysis": {...},
    "skills_gap": {...},
    "courses": {...},
    "report_url": "/outputs/{job_id}/report.html"
  }
}
```

### Endpoint: `/api/analyze/stream/{job_id}`

**Method:** `GET`

**Description:** Server-sent events stream for real-time progress updates

**Response:** Stream of live updates as agents complete tasks

---

## 📁 Project Structure

```
Multi Agent With Crewai Framework/
├── main.py                 # FastAPI application & API endpoints
├── crew_logic.py           # CrewAI agents and task definitions
├── requirements.txt        # Python dependencies
├── run.bat                 # Batch file to start the server
├── .env                    # Environment variables (create this)
├── static/
│   └── index.html         # Web UI
└── outputs/
    └── {job_id}/          # Analysis results per job
        ├── step_1_company.json
        ├── step_2_skills_gap.json
        ├── step_3_courses.json
        └── step_4_report.html
```

---

## 🤖 How It Works

### Agent Pipeline

1. **Company Analyzer Agent**
   - Searches for company information and job postings
   - Extracts required skills from job descriptions
   - Creates a summary of company's skill needs

2. **Skills Gap Detector Agent**
   - Analyzes extracted skills
   - Prioritizes based on frequency and importance
   - Generates search queries for relevant courses

3. **Course Finder Agent**
   - Searches Coursera and Udemy
   - Scrapes course details and ratings
   - Ranks courses by relevance and quality

4. **Training Report Author Agent**
   - Compiles all findings
   - Generates professional HTML report
   - Provides actionable training recommendations

### Data Flow

```
Company Request
    ↓
Company Analyzer Agent → step_1_company.json
    ↓
Skills Gap Detector → step_2_skills_gap.json
    ↓
Course Finder Agent → step_3_courses.json
    ↓
Report Author Agent → step_4_report.html
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **CrewAI** | Multi-agent orchestration framework |
| **FastAPI** | High-performance web API |
| **OpenAI GPT-4** | LLM for agent reasoning |
| **Tavily** | Web search and information retrieval |
| **ScrapeGraphAI** | AI-powered web scraping |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI web server |

---

## 📊 Output Files

The analysis generates four output files per job:

1. **step_1_company.json** — Company analysis with job posts and skills
2. **step_2_skills_gap.json** — Prioritized skill gaps with reasoning
3. **step_3_courses.json** — Recommended courses with details
4. **step_4_report.html** — Professional HTML report (ready to share)

---

## 🔧 Configuration & Customization

### Adjust Analysis Parameters

In `main.py`, modify the `AnalysisRequest` model defaults:

```python
class AnalysisRequest(BaseModel):
    min_job_posts: int = 1        # Increase for more job posts
    top_skills_no: int = 2        # More skills to analyze
    top_courses_no: int = 2       # More courses per skill
    top_platforms_no: int = 2     # More platforms to search
```

### Customize Agent Behavior

Edit `crew_logic.py` to:
- Change agent roles and goals
- Modify task descriptions
- Adjust LLM parameters (temperature, model)
- Add new tools or data sources

---

## 🐛 Troubleshooting

### API Keys Not Found
- Ensure `.env` file exists in project root
- Verify all required API keys are set correctly
- Restart the server after updating `.env`

### Slow Analysis
- Reduce `min_job_posts` and `top_courses_no` parameters
- Analysis time depends on API response speeds
- Check API rate limits for Tavily and OpenAI

### Course Scraping Errors
- Verify `SGAI_API_KEY` is valid
- Some websites may block scraping
- Check `top_platforms_no` is not too high

---

## 📝 Example Usage

### Via cURL

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "industry": "Technology",
    "min_job_posts": 3,
    "top_skills_no": 5,
    "top_courses_no": 3,
    "top_platforms_no": 2
  }'
```

### Via Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "company_name": "Microsoft",
        "industry": "Software Development",
        "min_job_posts": 2,
        "top_skills_no": 3,
        "top_courses_no": 2,
        "top_platforms_no": 2
    }
)

job_id = response.json()["job_id"]
print(f"Analysis started: {job_id}")
```

---

## 📜 License

This project is open-source and available for personal and commercial use.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

---

## 📧 Support

For issues, questions, or feedback, please open an issue in the project repository or contact the development team.

---

**Built with Jana Ashraf**
#   M u l t i - A g e n t - W i t h - C r e w a i  
 