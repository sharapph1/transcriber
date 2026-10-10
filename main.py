import soundfile as sf
from kokoro import KPipeline

# Initialize pipeline for Hindi ('h')
pipeline = KPipeline(lang_code='h') 

text = "नमस्ते, यह कोकoro टीडीएस का स्थानीय परीक्षण है।"
generator = pipeline(text, voice='hf_alpha', speed=1.0) # Updated valid voice code

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f'output_{i}.wav', audio, 24000)
    print(f"Generated chunk {i} successfully!")
