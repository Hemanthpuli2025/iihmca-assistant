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

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("message", "").strip().lower()

    keywords_map = {
        ("admission", "open", "start"): "Admissions are open from June 1st to July 15th.",
        ("courses", "programs", "culinary"): "We offer BHM, BCT&CA, Diploma in Culinary Arts, and Hotel Management.",
        ("hostel", "accommodation"): "Yes, IIHMCA offers hostel facilities for both boys and girls.",
        ("fee", "fees", "structure", "cost"): "The fee structure varies by course. Please visit our website or contact the admin office.",
        ("placement", "job", "career"): "Yes, we have a strong placement cell that supports job placements after course completion.",
        ("contact", "phone", "email", "number"): "You can reach us at +91-XXXXXXXXXX or email us at info@iihmca.org.",
        ("entrance", "exam", "test"): "No, admissions are based on merit and a personal interview.",
        ("eligibility", "qualification"): "You must have completed 10+2 from any recognized board to apply for our degree programs.",
    }

    reply = "Sorry, I didn't understand your question. Could you please rephrase it?"

    for keywords, answer in keywords_map.items():
        if any(keyword in question for keyword in keywords):
            reply = answer
            break

    return JSONResponse({"reply": reply})