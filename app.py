from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "*"]}})

@app.get("/health")
def health():
    return jsonify({"ok": True})


def _analyze_only(query: str):
    from services.signavio import fetch_process_data, send_to_llm_context
    from services.llm import chat_complete
    raw = fetch_process_data(query)
    context = send_to_llm_context(raw)
    messages = [
        {"role": "system", "content": "You are a Process Intelligence Analyst. "
         "Return JSON with keys: summary (string), bullets (list), actions (list), narration (string)."},
        {"role": "user", "content": f"Analyze:\n{context}"},
    ]
    import json
    content = chat_complete(messages)
    parsed = json.loads(content)
    return raw, parsed

@app.post("/analyze")
def analyze():
    data = request.get_json(force=True) or {}
    query = data.get("query", "Show weekly bottlenecks")
    raw, analysis = _analyze_only(query)
    return jsonify({"raw": raw, "analysis": analysis})

@app.post("/ppt")
def ppt():
    from services.pptgenerator import generate_ppt   # ✱ lazy import
    payload = request.get_json(force=True) or {}
    title = payload.get("title", "Process Intelligence – Bottlenecks")
    summary = payload.get("summary", "Weekly insights")
    bullets = payload.get("bullets", [])
    kpis = payload.get("kpis", {})
    filename = payload.get("filename", "bottlenecks.pptx")
    path = generate_ppt(title, summary, bullets, kpis, filename, output_dir=OUTPUT_DIR)
    return jsonify({"ppt_path": path})

@app.get("/download")
def download():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True)

@app.post("/tts")
def tts():
    from services.tts import synthesize_tts     # ✱ lazy import
    payload = request.get_json(force=True) or {}
    text = payload.get("text", "No narration provided.")
    filename = payload.get("filename", "narration.mp3")
    try:
        path = synthesize_tts(text, filename=filename)
        return jsonify({"audio_path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.post("/run-agent")
def run_agent_route():
    # lazy import
    from agent import run_agent
    payload = request.get_json(force=True) or {}
    query = payload.get("query", "Weekly bottlenecks")
    make_ppt_flag = bool(payload.get("make_ppt", True))
    narrate_flag = bool(payload.get("narrate", True))
    try:
        result = run_agent(query, make_ppt_flag, narrate_flag)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=8000, debug=True)
