import os
import json
import uuid
import time
import asyncio
from threading import Thread
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crew_logic import run_crew_analysis

app = FastAPI(title="Corporate Training Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: dict = {}

class AnalysisRequest(BaseModel):
    company_name: str
    industry: str
    min_job_posts: int = 1
    top_skills_no: int = 2
    top_courses_no: int = 2
    top_platforms_no: int = 2


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/index.html")


@app.post("/api/analyze")
async def start_analysis(request: AnalysisRequest):
    job_id = str(uuid.uuid4())
    output_dir = os.path.join("outputs", job_id)

    jobs[job_id] = {
        "status": "running",
        "messages": [],
        "current_agent": None,
        "completed_agents": [],
        "result": None,
        "error": None,
        "output_dir": output_dir,
        "started_at": time.time(),
    }

    def progress_cb(msg_type: str, content: str, agent: Optional[str]):
        jobs[job_id]["messages"].append({
            "type": msg_type,
            "content": content,
            "agent": agent,
            "ts": time.time(),
        })
        if agent:
            jobs[job_id]["current_agent"] = agent

    def task_done_cb(agent_name: str):
        jobs[job_id]["completed_agents"].append(agent_name)
        jobs[job_id]["messages"].append({
            "type": "task_done",
            "content": f"{agent_name} completed successfully.",
            "agent": agent_name,
            "ts": time.time(),
        })

    def run_job():
        try:
            result = run_crew_analysis(
                inputs={
                    "company_name": request.company_name,
                    "industry": request.industry,
                    "min_job_posts": request.min_job_posts,
                    "top_skills_no": request.top_skills_no,
                    "top_courses_no": request.top_courses_no,
                    "top_platforms_no": request.top_platforms_no,
                },
                output_dir=output_dir,
                progress_cb=progress_cb,
                task_done_cb=task_done_cb,
            )
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)
            jobs[job_id]["messages"].append({
                "type": "error",
                "content": f"Error: {str(e)}",
                "agent": None,
                "ts": time.time(),
            })

    Thread(target=run_job, daemon=True).start()
    return {"job_id": job_id, "status": "started"}


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "status": job["status"],
        "current_agent": job["current_agent"],
        "completed_agents": job["completed_agents"],
        "error": job["error"],
        "elapsed": round(time.time() - job["started_at"]),
    }


@app.get("/api/stream/{job_id}")
async def stream_progress(job_id: str):
    """Server-Sent Events endpoint for real-time progress."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        last_idx = 0
        while True:
            job = jobs.get(job_id, {})
            messages = job.get("messages", [])

            # Stream new messages
            for msg in messages[last_idx:]:
                yield f"data: {json.dumps(msg)}\n\n"
            last_idx = len(messages)

            # Always send a heartbeat status
            status_evt = {
                "type": "status",
                "status": job.get("status"),
                "current_agent": job.get("current_agent"),
                "completed_agents": job.get("completed_agents", []),
                "elapsed": round(time.time() - job.get("started_at", time.time())),
            }
            yield f"data: {json.dumps(status_evt)}\n\n"

            if job.get("status") in ("completed", "failed"):
                final = {
                    "type": "final",
                    "status": job.get("status"),
                    "result": job.get("result"),
                    "error": job.get("error"),
                }
                yield f"data: {json.dumps(final)}\n\n"
                break

            await asyncio.sleep(1.5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed yet")
    return job["result"]


@app.get("/api/report/{job_id}", response_class=HTMLResponse)
async def get_report(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    report_path = os.path.join(job["output_dir"], "step_4_report.html")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not generated yet")
    with open(report_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
