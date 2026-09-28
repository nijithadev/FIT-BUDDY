from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
from openai import OpenAI

import os


# =========================================================
# 1. LOAD ENVIRONMENT VARIABLES
# =========================================================

# Always load .env from the same folder as this app.py file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

api_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI client only when a key is available.
client = OpenAI(api_key=api_key) if api_key else None


# =========================================================
# 2. CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Fit Buddy AI",
    description="Generative AI Fitness Assistant",
    version="1.0"
)


# =========================================================
# 3. CONNECT STATIC FOLDER
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)


# =========================================================
# 4. CONNECT JINJA2 TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


# =========================================================
# 5. HOME / DASHBOARD PAGE
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "error": None
        }
    )


# =========================================================
# 6. GENERATE FITNESS PLAN
# =========================================================

@app.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,

    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    goal: str = Form(...),
    activity_level: str = Form(...),
    food_preference: str = Form(...)
):

    # -----------------------------------------------------
    # Validate Age
    # -----------------------------------------------------

    if age < 10 or age > 100:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": None,
                "error": "Please enter a valid age between 10 and 100."
            }
        )


    # -----------------------------------------------------
    # Validate Weight and Height
    # -----------------------------------------------------

    if weight <= 0 or height <= 0:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": None,
                "error": "Height and weight must be greater than zero."
            }
        )


    # -----------------------------------------------------
    # Check OpenAI API Key
    # -----------------------------------------------------

    if client is None:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": None,
                "error": (
                    "OpenAI API key not found. "
                    "Please create a .env file beside app.py "
                    "and add OPENAI_API_KEY=your_key."
                )
            }
        )


    # =====================================================
    # 7. CREATE AI PROMPT
    # =====================================================

    prompt = f"""
You are Fit Buddy AI, a friendly fitness and wellness assistant.

Create a simple beginner-friendly fitness and wellness plan
based on the user's information.

USER DETAILS:

Name: {name}
Age: {age}
Gender: {gender}
Weight: {weight} kg
Height: {height} cm
Fitness Goal: {goal}
Activity Level: {activity_level}
Food Preference: {food_preference}

Create the response using the following sections:

1. Welcome Message

2. Fitness Goal

3. Daily Workout
- Exercise name
- Duration
- Number of days per week
- Simple instructions

4. Food Suggestions
- Breakfast
- Lunch
- Evening Snack
- Dinner

5. Daily Routine

6. Water and Hydration

7. Sleep

8. Safety Tips

Keep the explanation simple and beginner-friendly.

Give general wellness information only.

Do not diagnose diseases.
Do not prescribe medicines.
Do not recommend unsafe diets.
Do not suggest extreme weight loss or weight gain methods.

Mention that professional advice should be taken when necessary.
"""


    # =====================================================
    # 8. SEND REQUEST TO OPENAI
    # =====================================================

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        result = response.output_text


    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": None,
                "error": f"AI Error: {str(e)}"
            }
        )


    # =====================================================
    # 9. DISPLAY AI RESULT
    # =====================================================

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result,
            "error": None
        }
    )


# =========================================================
# 10. HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "success",
        "message": "Fit Buddy AI is running successfully"
    }
