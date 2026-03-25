import os
import uuid
import time

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.config import settings
from app.logger import app_logger

from app.services.resume_parser import extract_text
from app.services.profile_builder import build_profile
from app.services.scorer import ScoringAgent
from app.services.matcher import Matcher


# Ensure temp folder exists
os.makedirs(settings.TEMP_DIR, exist_ok=True)


router = APIRouter()

scoring_agent = ScoringAgent()
matcher = Matcher()


# ================================
# Candidate Scoring Endpoint
# ================================
@router.post("/score")
async def score_candidate(
    name: str = Form(...),
    email: str = Form(...),
    experience: float = Form(...),
    expected_ctc: float = Form(...),
    skills: str = Form(...),
    education: str = Form(...),
    resume: UploadFile = File(...)
):

    start_time = time.time()

    # Save uploaded resume
    file_id = str(uuid.uuid4())

    file_path = os.path.join(
        settings.TEMP_DIR,
        f"{file_id}.pdf"
    )

    with open(file_path, "wb") as f:
        f.write(await resume.read())

    # Extract resume text
    resume_text = extract_text(file_path)

    # Build form data
    form_data = {
        "name": name,
        "email": email,
        "experience": experience,
        "expected_ctc": expected_ctc,
        "skills": skills,
        "education": education
    }

    # Build profile
    profile = build_profile(form_data, resume_text)

    # AI Scoring
    result = scoring_agent.score(profile)

    # Store candidate for JD matching
    matcher.add_candidate(
        profile_text=profile,
        meta={
            "name": name,
            "email": email,
            "ai_score": result["total_score"],
            "experience": experience
        }
    )

    duration = round(time.time() - start_time, 2)

    app_logger.info(
        f"Scored {name} => {result['total_score']} in {duration}s"
    )

    return JSONResponse(result)


# ================================
# Job Description Matching
# ================================
@router.post("/match_jd")
def match_job_description(data: dict):

    if "job_description" not in data:
        return JSONResponse(
            status_code=400,
            content={"error": "job_description field required"}
        )

    jd_text = data["job_description"]

    results = matcher.match_jd(jd_text)

    app_logger.info(
        f"JD matched against {len(results)} candidates"
    )

    return JSONResponse(results)
