import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI


# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please create a .env file and add your API key."
    )


# Create OpenAI client
client = OpenAI(api_key=api_key)


# Create FastAPI application
app = FastAPI(
    title="AI Explanation Analyzer",
    description="Analyze and improve student explanations using AI",
    version="1.0"
)


# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Data received from frontend
class ExplanationRequest(BaseModel):
    topic: str
    explanation: str


# Home page
@app.get("/")
def home():
    return FileResponse("index.html")


# Analyze explanation
@app.post("/analyze")
def analyze_explanation(request: ExplanationRequest):

    prompt = f"""
You are an expert teacher and educational evaluator.

Analyze the student's explanation about the topic:

Topic:
{request.topic}

Student's Explanation:
{request.explanation}

Evaluate the explanation using these categories:

1. Accuracy
2. Clarity
3. Completeness
4. Grammar
5. Simplicity

Give each category a score from 1 to 10.

Then provide:

- Overall score out of 10
- Strengths
- Mistakes or incorrect information
- Missing important points
- Grammar/language improvements
- A simple explanation
- An improved version of the student's answer

IMPORTANT:
Do not invent facts.
If the student's explanation is correct, clearly say so.
Use simple language suitable for a student.

Return the result in this format:

ACCURACY: X/10
CLARITY: X/10
COMPLETENESS: X/10
GRAMMAR: X/10
SIMPLICITY: X/10
OVERALL SCORE: X/10

STRENGTHS:
- ...

MISTAKES:
- ...

MISSING POINTS:
- ...

GRAMMAR IMPROVEMENTS:
- ...

SIMPLE EXPLANATION:
...

IMPROVED ANSWER:
...
"""

    try:

        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )

        return {
            "success": True,
            "result": response.output_text
        }

    except Exception as error:

        return {
            "success": False,
            "result": str(error)
        }
load_dotenv()


print("API KEY LOADED:", os.getenv("OPENAI_API_KEY"))

api_key = os.getenv("OPENAI_API_KEY")

