import json
from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS (for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Change this IP if needed
OLLAMA_URL = os.getenv("OLLAMA_URL",
                         "http://192.168.219.7:11434/api/generate"
                         )


@app.get("/")
def root():
    return {"status": "LLM Backend Running"}


@app.post("/chat")
def chat(data: dict):
    prompt = data.get("prompt")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt
            },
            stream=True
        )

        full_response = ""

        # 🔥 Handle streaming response from Ollama
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    if "response" in json_data:
                        full_response += json_data["response"]
                except:
                    pass

        return {"response": full_response}

    except Exception as e:
        return {"error": str(e)}