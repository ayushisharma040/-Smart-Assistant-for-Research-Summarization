# 📄 Smart Assistant for Research Summarization

An AI-powered assistant that allows users to upload research papers or technical documents (PDF or TXT) and interact with them intelligently. It supports:

* Summarization (≤150 words)
* Q\&A with justification from source
* Logical reasoning and comprehension question generation
* Feedback on user answers

---

## 🛠️ Features

* ✅ **Upload PDF/TXT** files
* ✅ **Auto-summary** of document
* ✅ **Ask Anything**: Ask free-form questions with context-based answers
* ✅ **Challenge Me**: Get logic-based questions from the document
* ✅ **Evaluation**: Feedback on user’s answers with justification

---

## 🧱 Tech Stack

* Frontend: **Streamlit**
* Backend: **Python** (LangChain, OpenAI, FAISS)
* Document Parsing: **PyMuPDF**, **TextLoader**

---

## 📁 Project Structure

```
smart-assistant/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # All dependencies
├── README.md                # This file
└── utils/                   # Helper modules (optional)
```

---

## 🚀 How to Run Locally

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd smart-assistant
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App

```bash
streamlit run app.py
```

bash
git add postman_collection.json
git commit -m "Added Postman collection"
git push origin main


### 4. Add OpenAI API Key

* Paste your key in the sidebar input to begin using the assistant.

---

## ✅ Justification Example

Every answer includes the supporting paragraph/page number:

> "This is supported by paragraph 2 of section 3."

---

## 🧠 Bonus Feature Ideas (Optional)

* 🔁 Chat memory retention
* 🔎 Highlight exact text snippets in answers
* 🧪 Unit tests for QA pipeline

---

## 📹 Demo Walkthrough Script (Optional)

1. Upload a PDF (e.g., sample research paper)
2. Watch the auto-summary populate
3. Try free-form Q\&A — ask something like: *"What is the main methodology used?"*
4. Switch to “Challenge Me” mode and answer the generated questions
5. Watch how the assistant gives feedback with evidence

---

## 📬 Contact

Made with ❤️ for EZ by Ayushi Sharma
