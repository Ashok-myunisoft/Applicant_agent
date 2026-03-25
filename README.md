# AI Applicant Scoring System

## Setup

### 1. Install Ollama
https://ollama.com

ollama pull llama3

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run

uvicorn app.main:app --reload

### 4. API

POST /score
Form-data:
- name
- email
- experience
- expected_ctc
- skills
- education
- resume


#### Start Ollama

ollama serve

### Run API
uvicorn app.main:app --reload


http://127.0.0.1:8000/docs


