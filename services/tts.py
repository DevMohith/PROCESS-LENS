import os
from typing import Optional
from elevenlabs import ElevenLabs, save, VoiceSettings
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def synthesize_tts(text: str, filename: str = "narration.mp3", voice_id: Optional[str] = None) -> str:
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("Missing ELEVENLABS_API_KEY; please set it in .env")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    voice_id = "FTNCalFNG5bRnkkaP5Ug"

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        optimize_streaming_latency="0",
        output_format="mp3_44100_128",
        text=text,
        voice_settings=VoiceSettings(
            stability=0.55,
            similarity_boost=0.65,
            style=0.3,
            use_speaker_boost=True,
        ),
    )

    out_path = os.path.join(OUTPUT_DIR, filename)
    save(audio, out_path)
    return out_path