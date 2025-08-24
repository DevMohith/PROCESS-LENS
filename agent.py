from typing import Dict, List, Tuple
from services.signavio import fetch_process_data, send_to_llm_context
from services.llm import chat_complete
from services.pptgenerator import generate_ppt
from services.tts import synthesize_tts
import json

system_prompt = """You are a Process Intelligence Analyst Agent.
You receive structured process telemetry (KPIs, bottlenecks, variants).
Your job:
1) Summarize in 3-5 crisp bullet points for executives.
2) Recommend 3 actionable fixes (who should do what & why).
3) Provide a short narrator script (60-120 words) suitable for TTS.
Output strictly in JSON with keys:
{
  "summary": "...",
  "bullets": ["...", "...", "..."],
  "actions": ["...", "...", "..."],
  "narration": "..."
}
"""

#analyzing process carries - data collection and send them to llm for making the output professional
def analyze_process(query: str) -> Tuple[Dict, Dict]:
    raw = fetch_process_data(query)
    context = send_to_llm_context(raw)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User query: {query}\n\nDATA:\n{context}"},
    ]
    content = chat_complete(messages)
    parsed = json.loads(content)
    return raw, parsed


#here agent uses tools and calls Text to speech and reads out the bottlenecs proposed by llm and alongside generates ppt
def run_agent(query: str, generate_ppt_flag: bool, narrate_flag: bool) -> Dict:
    raw, analysis = analyze_process(query)

    result = {
        "kpis": raw.get("kpis", {}),
        "summary": analysis.get("summary", ""),
        "bullets": analysis.get("bullets", []),
        "actions": analysis.get("actions", []),
        "narration": analysis.get("narration", ""),
        "ppt_path": None,
        "audio_path": None,
    }
    
    # triggers
    if generate_ppt_flag:
        title = f"{raw.get('process')} Weekly Bottlenecks"
        filename = "process_bottlenecks.pptx"
        ppt_path = generate_ppt(title, result["summary"], result["bullets"] + result["actions"], raw.get("kpis", {}), filename)
        result["ppt_path"] = ppt_path

    if narrate_flag and result["narration"]:
        audio_path = synthesize_tts(result["narration"], filename="narration.mp3")
        result["audio_path"] = audio_path

    return result
