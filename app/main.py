from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title="AI Applicant Scoring System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
