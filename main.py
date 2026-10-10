import os
import soundfile as sf
from fastapi import FastAPI, Form, JSONResponse
from fastapi.responses import FileResponse
from kokoro import KPipeline

# Force strict offline mode to utilize your local cached model files
os.environ["HF_HUB_OFFLINE"] = "1"

app = FastAPI()

print("Loading Kokoro TTS model locally...")
pipeline = KPipeline(lang_code='h', repo_id='hexgrad/Kokoro-82M')
print("Model loaded successfully!")

@app.post("/generate")
async def generate_audio(text: str = Form(...), voice: str = Form("hf_alpha")):
    try:
        output_path = "output.wav"
        
        generator = pipeline(text, voice=voice, speed=1.0)
        for i, (gs, ps, audio) in enumerate(generator):
            sf.write(output_path, audio, 24000)
            break  # Take the first generated chunk
            
        return FileResponse(output_path, media_type="audio/wav", filename="speech.wav")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
