from fastapi import FastAPI, Request
import requests
import os
import random

app = FastAPI()

# ===== CONFIG =====

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"

SYSTEM_PROMPT = """
You are a savage roast AI.
Rules:
- Roast ONLY the last message sender
- No name listing
- No repeating lines
- Short, brutal, funny Hinglish roasts
- Emoji allowed
"""

# Fallback roasts (agar API fail ho)
FALLBACK = [
    "Bhai tu bolta kam aur confuse zyada karta hai 🤡",
    "Itna weak message? Recharge khatam ho gaya kya 😭",
    "Lagta hai tera dimaag airplane mode pe hai 🛫",
    "Tu bolta hai par sense nahi aata 💀",
    "इतना confidence और इतना zero content, wah 👏"
]

# ===== ROUTE =====

@app.post("/roast")
async def roast(req: Request):
    body = await req.json()
    msg = body.get("message", "")

    if not msg:
        return {"roast": random.choice(FALLBACK)}

    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": msg}
                ],
                "temperature": 1.1,
                "max_tokens": 120
            },
            timeout=20
        )

        data = r.json()
        roast = data["choices"][0]["message"]["content"]
        return {"roast": roast.strip()}

    except Exception as e:
        return {"roast": random.choice(FALLBACK)}