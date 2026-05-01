import os
import json
import uuid
import time
from threading import Thread
from typing import Callable
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from pydantic import BaseModel, Field
from typing import List, Optional
from tavily import TavilyClient
from scrapegraphai.graphs import SmartScraperGraph

load_dotenv()

OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
TAVILY_API_KEY   = os.getenv("TAVILY_API_KEY")
SGAI_API_KEY     = os.getenv("SGAI_API_KEY")

os.environ["OPENAI_API_KEY"]   = OPENAI_API_KEY
os.environ["AGENTOPS_API_KEY"] = AGENTOPS_API_KEY
os.environ["TAVILY_API_KEY"]   = TAVILY_API_KEY
os.environ["SGAI_API_KEY"]     = SGAI_API_KEY

_search_client = TavilyClient(api_key=TAVILY_API_KEY)

_scrapegraphai_config = {
    "llm": {
        "model": "openai/gpt-4o-mini",
        "api_key": OPENAI_API_KEY,
        "temperature": 0,
    },
}

class SingleJobPost(BaseModel):
    job_title: str
    required_skills: List[str] = Field(..., title="Required skills from the job post")
    experience_level: str = Field(..., title="e.g. Junior, Mid, Senior")
    source_url: str

class CompanyAnalysisResult(BaseModel):
    comapany_name: str
    industery: str
    company_summary: str = Field(..., title="Brief summary about the company")
    job_posts: List[SingleJobPost]
    top_required_skills: List[str] = Field(..., title="Most frequently required skills")

class SingleSkillGap(BaseModel):
    skill_name: str
    importance_level: str = Field(..., title="High / Medium / Low")
    reason: str = Field(..., title="Why this skill is a priority")
    suggested_search_queries: List[str] = Field(..., title="Search queries to find courses", min_items=1, max_items=2)

class SkillsGapReport(BaseModel):
    total_skills_found: int
    priority_skills_for_training: List[SingleSkillGap]

class SingleCourse(BaseModel):
    skill_name: str = Field(..., title="The skill this course addresses")
    course_title: str
    platform: str
    course_url: str
    price: Optional[str] = Field(default=None)
    duration: Optional[str] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    level: Optional[str] = Field(default=None)
    agent_recommendation_rank: int
    agent_recommendation_notes: List[str]

class AllCoursesResult(BaseModel):
    total_courses_found: int
    courses: List[SingleCourse]


@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query."""
    return _search_client.search(query)

@tool
def web_scraping_tool(page_url: str):
    """An AI tool to scrape a web page and extract course details."""
    sga_prompt = "Extract ```json\n" + SingleCourse.schema_json() + "```\n From the web page"
    smart_scraper_graph = SmartScraperGraph(
        prompt=sga_prompt,
        source=page_url,           #  FIXED: was missing before
        config=_scrapegraphai_config,
    )
    details = smart_scraper_graph.run()   #  FIXED: no argument here
    return {"page_url": page_url, "details": details}


def run_crew_analysis(
    inputs: dict,
    output_dir: str,
    progress_cb: Callable,
    task_done_cb: Callable,
) -> dict:
    """
    Runs the full CrewAI analysis pipeline.
    Calls progress_cb(type, content, agent) for live updates.
    Calls task_done_cb(agent_name) when each task finishes.
    Returns a dict with structured results.
    """
    os.makedirs(output_dir, exist_ok=True)

    basic_llm = LLM(model="gpt-4o-mini", temperature=0)

    about_system = (
        "This is an AI-powered Corporate Training Analyzer that helps companies "
        "identify skill gaps and find the best training courses for their employees."
    )
    system_context = StringKnowledgeSource(content=about_system)

    # Analyze company and available job positions
    company_analyzer_agent = Agent(
        role="Company Analyzer Agent",
        goal="\n".join([
            "To analyze a company by searching for its LinkedIn job postings and general info.",
            "Extract all required skills from job posts to understand what the company needs.",
        ]),
        backstory="Helps HR teams understand what skills their company is actively hiring for.",
        llm=basic_llm,
        tools=[search_engine_tool],
    )
    company_analyzer_task = Task(
        description="\n".join([
            "Analyze the company: {company_name} in the {industry} industry.",
            "Search for their LinkedIn job postings and any other relevant job boards.",
            "Also search for general information about the company to write a brief summary.",
            "Extract required skills from EXACTLY {min_job_posts} job post only. Do NOT search for more.",
            "Focus on technical and soft skills mentioned in the job descriptions.",
            "Identify the most frequently required skills across the job post.",
        ]),
        expected_output="A JSON object containing the company analysis with job posts and required skills.",
        output_json=CompanyAnalysisResult,
        output_file=os.path.join(output_dir, "step_1_company.json"),
        agent=company_analyzer_agent,
    )

    # Identify skill gaps needed
    skills_gap_detector_agent = Agent(
        role="Skills Gap Detector Agent",
        goal="\n".join([
            "To analyze the required skills from job postings and identify the most critical ones.",
            "Prioritize skills based on frequency, market demand, and business impact.",
        ]),
        backstory="Helps companies understand which skills their employees need most.",
        llm=basic_llm,
        verbose=True,
    )
    skills_gap_detector_task = Task(
        description="\n".join([
            "Based on the company analysis results, identify the top skill gaps for {company_name}.",
            "Focus on the top {top_skills_no} most important skills that need training.",
            "For each skill, explain why it's a priority and generate ONLY 1-2 search queries.",
            "Consider both technical (hard) and professional (soft) skills.",
            "Order skills from highest to lowest priority.",
        ]),
        expected_output="A JSON object with the skills gap analysis.",
        output_json=SkillsGapReport,
        output_file=os.path.join(output_dir, "step_2_skills_gap.json"),
        agent=skills_gap_detector_agent,
    )

    # Find best courses for these skills
    course_finder_agent = Agent(
        role="Course Finder Agent",
        goal="To find the best training courses from ONLY {top_platforms_no} platforms for each skill gap.",
        backstory="Finds the most relevant cost-effective training courses based on skill gaps.",
        llm=basic_llm,
        tools=[search_engine_tool, web_scraping_tool],
        verbose=True,
    )
    course_finder_task = Task(
        description="\n".join([
            "Based on the skills gap report, find the best training courses for each skill.",
            "Search on ONLY {top_platforms_no} platforms: Coursera and Udemy. Do NOT search elsewhere.",
            "For each skill, find at most {top_courses_no} courses TOTAL. STOP after reaching this limit.",
            "Scrape at most 1 page per skill — do NOT scrape more pages.",
            "Ignore courses with very low ratings (below 4.0 if rating is available).",
            "Rank courses from best to worst based on rating, relevance, and price.",
            "Prioritize courses matching the company's industry: {industry}.",
            "IMPORTANT: Total scraping calls must NOT exceed {top_skills_no} x {top_platforms_no}.",
        ]),
        expected_output="A JSON object with the courses found for each skill gap.",
        output_json=AllCoursesResult,
        output_file=os.path.join(output_dir, "step_3_courses.json"),
        agent=course_finder_agent,
    )

    # Generate comprehensive training report
    training_report_author_agent = Agent(
        role="Training Report Author Agent",
        goal="To generate a professional HTML page for the corporate training plan report.",
        backstory="Generates richly formatted HTML reports summarizing training recommendations.",
        llm=basic_llm,
        verbose=True,
    )
    training_report_author_task = Task(
        description="\n".join([
            "Generate a professional HTML training plan report for {company_name}.",
            "Use Bootstrap CSS framework for a better UI.",
            "Include these sections:",
            "1. Executive Summary: Overview of the company and key findings.",
            "2. Company Profile: Brief description.",
            "3. Skills Gap Analysis: Detailed breakdown of skill gaps.",
            "4. Recommended Training Plan: Table of top courses per skill.",
            "5. Budget Estimation: Estimated total training investment.",
            "6. Implementation Timeline: Suggested rollout plan.",
            "7. Conclusion: Summary and next steps.",
            "Make the report visually appealing with colors, icons, and charts.",
        ]),
        expected_output="A professional HTML page for the corporate training plan report.",
        output_file=os.path.join(output_dir, "step_4_report.html"),
        agent=training_report_author_agent,
    )

    _agent_order = [
        "Company Analyzer Agent",
        "Skills Gap Detector Agent",
        "Course Finder Agent",
        "Training Report Author Agent",
    ]

    def step_callback(step_output):
        try:
            text = str(step_output)[:300]
            agent = getattr(step_output, "agent", None) or ""
            progress_cb("step", text, agent)
        except Exception:
            pass

    def task_callback(task_output):
        try:
            agent_name = str(getattr(task_output, "agent", "Unknown"))
            task_done_cb(agent_name)
        except Exception:
            pass

    crew = Crew(
        agents=[
            company_analyzer_agent,
            skills_gap_detector_agent,
            course_finder_agent,
            training_report_author_agent,
        ],
        tasks=[
            company_analyzer_task,
            skills_gap_detector_task,
            course_finder_task,
            training_report_author_task,
        ],
        process=Process.sequential,
        knowledge_sources=[system_context],
        step_callback=step_callback,
        task_callback=task_callback,
    )

    progress_cb("info", "🚀 Analysis started! Crew is being assembled...", None)
    result = crew.kickoff(inputs=inputs)

    output = {
        "company_name": inputs.get("company_name"),
        "industry": inputs.get("industry"),
        "skills": [],
        "courses": [],
        "report_path": os.path.join(output_dir, "step_4_report.html"),
    }

    # Read saved JSON files
    skills_path  = os.path.join(output_dir, "step_2_skills_gap.json")
    courses_path = os.path.join(output_dir, "step_3_courses.json")

    if os.path.exists(skills_path):
        with open(skills_path, "r", encoding="utf-8") as f:
            output["skills"] = json.load(f).get("priority_skills_for_training", [])

    if os.path.exists(courses_path):
        with open(courses_path, "r", encoding="utf-8") as f:
            output["courses"] = json.load(f).get("courses", [])

    return output
