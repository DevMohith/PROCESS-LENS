# ProcessLens – Bottleneck Agent (LLM + PPT + TTS)

## What this does
- Pulls (mocked) Signavio Process Intelligence data
- Uses an LLM (OpenRouter) to summarize KPIs, bottlenecks, actions
- Generates a PPT with python-pptx
- Narrates the insights via ElevenLabs TTS

# Fill OPENROUTER_API_KEY, ELEVENLABS_API_KEY
mkdir -p outputs
python app.py
