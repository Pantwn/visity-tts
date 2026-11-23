from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import edge_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/speak")
async def speak(data: dict):
    texto = data.get("text", "")
    voz = data.get("voice", "es-MX-JorgeNeural")
    rate = data.get("rate", "+0%")
    pitch = data.get("pitch", "+0Hz")
    communicate = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return Response(content=audio, media_type="audio/mpeg")

@app.get("/")
async def home():
    return {"ok": True, "voz": "visity-tts listo"}
