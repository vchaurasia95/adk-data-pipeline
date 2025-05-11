## 🧠 Event Processing Pipeline using Google ADK

This project demonstrates a fully modular, AI-agent-driven pipeline that processes raw user events through validation, deduplication, and session assignment — all orchestrated via [Google's Agent Development Kit (ADK)](https://cloud.google.com/vertex-ai/generative-ai/docs/agents/agent-development-kit).

### 🔧 What It Does

* ✅ Validates raw user events for required fields
* ✅ Deduplicates identical events (e.g., retries, replays)
* ✅ Groups events into user sessions based on time gaps
---

### 📁 Project Structure

```
.
├── agent.py                    # LLM agent definitions & orchestration
├── tools/
│   ├── validation_tool.py     # validate_events tool
│   ├── dedup_tool.py          # deduplicate_events tool
│   ├── session_tool.py        # assign_sessions tool
│   └── load_data.py           # load_event_file tool (for file/JSON input)
├── instructions/
│   ├── data_pipeline_instruct.txt
│   ├── validation_instruct.txt
│   ├── dedup_instruct.txt
│   └── session_instruct.txt
├── .env                        #File holding your Google API Key
├── input/
│   └── raw_events.json        # Sample input file
```

---

### 🚀 How It Works

1. **Pipeline Start**
   User provides raw event data via JSON or file upload.

2. **Validation Agent**
   Ensures all events have `user_id`, `event_type`, and `timestamp`.

3. **Deduplication Agent**
   Removes duplicate events using hashing logic.

4. **Session Agent**
   Groups user events into sessions based on inactivity (default: 30 min or configurable).
---

### 🧹 Agent Instructions

Each agent follows a declarative instruction template. Example:

```txt
You are the 'Event Validation Agent' in a user analytics data pipeline.
You will receive a list of raw user events as input.
Your job is to return:
{
  "valid_events": [...],
  "invalid_events": [...]
}
Print ONLY the result using your output_key.
```

See `/instructions/*.txt` for full definitions.

---

### ⚙️ Setup & Run

> Ensure .env file has the google API key.

```bash
pip install -r requirements.txt
adk web
```

> Ensure your environment supports Google ADK (`google-adk` Python package) and you have proper authentication.

---

### 📆 Features Used

* **ADK Agents & Tools** (`LlmAgent)
* **Sub-Agent Orchestration**
* **Session Memory & State Passing**

---

### 🙌 Inspired By

* Google ADK documentation
* Real-world event ingestion and transformation pipelines
* Agentic AI development best practices

---

### 📜 License

MIT — feel free to adapt or fork!
