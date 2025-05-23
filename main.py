import openai
import os

# Replace this with your actual API key from https://platform.openai.com/account/api-keys
openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("message", "").strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI admission assistant for IIHMCA, a hospitality and culinary college in Hyderabad, India. You help students with questions about admissions, courses, placements, hostel, fee structure, and eligibility. Answer like a helpful counselor. If the question is unclear, politely ask them to rephrase."
                },
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Sorry, there was an error: {e}"

    return JSONResponse({"reply": reply})