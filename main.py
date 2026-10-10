import os
import soundfile as sf
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from kokoro import KPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

print("Loading Kokoro TTS model...")
pipeline = KPipeline(lang_code='h', repo_id='hexgrad/Kokoro-82M')
print("Model loaded successfully!")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/generate")
async def generate_audio(text: str = Form(...), voice: str = Form("hf_alpha")):
    try:
        output_path = "output.wav"
        generator = pipeline(text, voice=voice, speed=1.0)
        for _, _, audio in generator:
            sf.write(output_path, audio, 24000)
            break
        return FileResponse(output_path, media_type="audio/wav", filename="speech.wav")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
