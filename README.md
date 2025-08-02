🧠 Agentified: Full-Stack AI Code Generator

Agentified is an experimental project that uses LangChain, Google Gemini, and multiple AI agents to generate full-stack web applications — from product requirements to frontend, backend, test code, and user stories — with human approval steps along the way.

🚀 Features

- 📝 Natural Language to Code : Just type your product idea — e.g., “Nocode tool to generate synthetic data” — and the system does the rest.
- 📋 User Story Generator : Automatically generates Agile-style user stories.
- 💻 Frontend + Backend Generation : Produces FastAPI backend and Tailwind/React frontend code.
- 🧪 Test Case Generator : Writes integration & unit tests with validation and logging.
- 🧑‍⚖️ Human-in-the-Loop Approval : Approve or reject each module before moving to the next.
- 📁 Build Output Saved : All approved code is saved to a `./build/` directory.

---

🛠️ Tech Stack

- LangChain (RunnableSequence-based chains)
- Google Generative AI / Gemini Pro
- Python 3.10+
- FastAPI(for backend generation)
- Pydantic(for schema validation)
- TailwindCSS / React(optional frontend targets)
- Pytest(for test generation)
---
📦 Installation

```bash
git clone https://github.com/yourusername/agentified.git
cd agentified
pip install -r requirements.txt
````

Ensure you have:

* Python 3.10+
* A valid Google Gemini API key

---
▶️ Running the Agent Pipeline

```bash
python main.py
```

You'll be prompted like:

```
📌 Enter product requirements:
```

Type something like:

```
nocode tool to generate synthetic data for anti-money laundering ML models
```

Then follow the prompts and approve the generated code step-by-step.

---
📁 Output Structure

After successful generation and approval, files will be saved to:

```
/build
├── userstories.txt
├── frontend.txt
├── backend.txt
├── tests.txt
```

---

🧪 Running Tests

If you’ve approved backend + tests:

```bash
pytest build/tests.txt  # Assuming converted properly to .py format
```

---

🧩 Folder Structure

```
agentified/
├── main.py
├── agents/
│   ├── frontend_agent.py
│   ├── backend_agent.py
│   ├── testing_agent.py
│   └── userstories_agent.py
├── utils/
│   ├── formatters.py
│   └── hitl.py
├── workflows/
│   └── full_build.py
└── build/
    └── *.txt (generated output)
```

---

❗ Known Issues

* `LangChainDeprecationWarning` on `LLMChain` — replaced by `RunnableSequence` in latest update.
* Ensure correct input variables (`{code}`) in prompt templates.
* Gemini `chat-bison-001` is deprecated — use `gemini-pro` instead.
* FastAPI logs may need CORS and LoggingMiddleware fixes when deploying.

---

✅ Future Features

* 🌐 Auto-deploy to Vercel / Railway / Replit
* 🧩 Plugin system for agents
* 🤖 Voice input for requirements
* 🌍 Support for multi-language codegen (Node, Go, etc.)

---

🧑‍💻 Contributing

Pull requests welcome! To add a new agent:

1. Create agent in `agents/`
2. Add logic in `full_build.py`
3. Register output in `main.py` for saving

---

📄 License

MIT License © 2025 \Manoj Kurapati 