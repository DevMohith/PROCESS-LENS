import React, { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function App() {
  const [query, setQuery] = useState("Last week bottlenecks in P2P");
  const [emails, setEmails] = useState("owner@company.com");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [pptLink, setPptLink] = useState(null);
  const [log, setLog] = useState([]);

  const pushLog = (m) => setLog((l) => [m, ...l]);

  const parseEmails = () =>
    emails
      .split(/[,\s]+/)
      .map((e) => e.trim())
      .filter(Boolean);

  // Button 1: Analyze + Narrate only
  const handleNarrate = async () => {
    setLoading(true);
    setPptLink(null);
    setAudioUrl(null);
    setAnalysis(null);

    try {
      // Use your existing /analyze + /tts combo, or /run-agent with narrate only.
      const res = await axios.post(`${API}/run-agent`, {
        query,
        make_ppt: false,
        narrate: true,
      });

      pushLog("Agent finished narration step.");
      if (res.data?.analysis) setAnalysis(res.data.analysis);

      // If your /run-agent returns audio_path, build a /download URL for the audio:
      if (res.data?.audio_path) {
        const url = `${API}/download?path=${encodeURIComponent(res.data.audio_path)}`;
        setAudioUrl(url);
      }
    } catch (e) {
      console.error(e);
      pushLog(`Narrate error: ${e.response?.data?.error || e.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Button 2: Generate PPT & optionally email it
  const handlePptAndEmail = async () => {
    setLoading(true);
    setPptLink(null);

    try {
      const res = await axios.post(`${API}/run-agent`, {
        query,
        make_ppt: true,
        narrate: false,
        emails: parseEmails(),
      });

      pushLog("Agent finished PPT step.");
      if (res.data?.ppt_path) {
        const url = `${API}/download?path=${encodeURIComponent(res.data.ppt_path)}`;
        setPptLink(url);
      }
      if (res.data?.email) {
        pushLog(`Email status: ${res.data.email.sent ? "sent" : `not sent (${res.data.email.reason})`}`);
      }
      if (res.data?.analysis) setAnalysis(res.data.analysis);
    } catch (e) {
      console.error(e);
      pushLog(`PPT error: ${e.response?.data?.error || e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Inter, system-ui, sans-serif", padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <h1>ProcessLens – Bottleneck Agent</h1>

      <label style={{ display: "block", fontWeight: 600, marginTop: 16 }}>Query</label>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        placeholder="e.g., Last week bottlenecks in P2P"
      />

      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <button onClick={handleNarrate} disabled={loading} style={btnStyle}>
          🔊 Analyze & Narrate
        </button>
        <button onClick={handlePptAndEmail} disabled={loading} style={btnStyle}>
          📊 Generate PPT & Email
        </button>
      </div>

      <label style={{ display: "block", fontWeight: 600, marginTop: 20 }}>Email recipients (comma or space separated)</label>
      <input
        value={emails}
        onChange={(e) => setEmails(e.target.value)}
        style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        placeholder="owner@company.com manager@company.com"
      />

      {loading && <p style={{ marginTop: 16 }}>Working…</p>}

      {analysis && (
        <div style={card}>
          <h3>Analysis</h3>
          {analysis.summary && <p><strong>Summary:</strong> {analysis.summary}</p>}
          {(analysis.bullets || []).length > 0 && (
            <>
              <p><strong>Highlights:</strong></p>
              <ul>{analysis.bullets.map((b, i) => <li key={i}>{b}</li>)}</ul>
            </>
          )}
          {(analysis.actions || []).length > 0 && (
            <>
              <p><strong>Actions:</strong></p>
              <ul>{analysis.actions.map((a, i) => <li key={i}>{a}</li>)}</ul>
            </>
          )}
        </div>
      )}

      {audioUrl && (
        <div style={card}>
          <h3>Narration</h3>
          <audio src={audioUrl} controls />
        </div>
      )}

      {pptLink && (
        <div style={card}>
          <h3>Presentation</h3>
          <a href={pptLink}>⬇️ Download PPT</a>
        </div>
      )}

      <div style={{ ...card, marginTop: 24 }}>
        <h3>Activity</h3>
        <ul>
          {log.map((l, i) => (
            <li key={i}>{l}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

const btnStyle = {
  padding: "10px 14px",
  borderRadius: 8,
  border: "1px solid #999",
  background: "#111",
  color: "white",
  cursor: "pointer",
};

const card = {
  marginTop: 20,
  padding: 16,
  border: "1px solid #e4e4e4",
  borderRadius: 10,
  background: "#fafafa",
};
