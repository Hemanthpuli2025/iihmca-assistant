from openai import OpenAI

client = OpenAI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("message", "").strip()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI admission assistant for IIHMCA, a hospitality and culinary college in Hyderabad, India. You help students with questions about admissions, courses, placements, hostel, fee structure, and eligibility. Answer like a helpful counselor."
                },
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Sorry, there was an error: {e}"

    return JSONResponse({"reply": reply})