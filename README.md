# FAQ Chatbot (CodeAlpha AI Internship - Task 2)

A rule-based FAQ chatbot that matches user questions to the closest FAQ
using **NLP preprocessing (NLTK)** + **TF-IDF vectorization** +
**cosine similarity**, served through a Flask backend with a simple web
chat UI.

---

## 🧠 How it works (explain this to your mentor)

1. **FAQ dataset** (`faq_data.json`) — a list of question/answer pairs
   about the CodeAlpha internship (tasks, certificates, GitHub, etc.).
2. **Preprocessing** (`preprocess()` in `app.py`) — every question (both
   the FAQ questions and the user's typed question) is:
   - lowercased
   - stripped of punctuation
   - tokenized (split into words) using NLTK
   - stopwords removed (common filler words like "is", "the", "a")
   - lemmatized (words reduced to root form, e.g. "certificates" → "certificate")
3. **Vectorization** — all cleaned FAQ questions are converted into
   numeric vectors using **TF-IDF** (`TfidfVectorizer` from scikit-learn).
   TF-IDF gives more weight to distinctive words and less weight to common
   ones.
4. **Matching** — when a user asks something, it's cleaned and vectorized
   the same way, then compared to every FAQ vector using **cosine
   similarity** (a score from 0 to 1 measuring how similar two vectors
   are). The FAQ with the highest score is returned as the answer.
5. **Fallback** — if the best score is below a threshold (0.25), the bot
   admits it doesn't know instead of returning a wrong answer.

---

## 📁 Project structure

```
FAQChatbot/
├── app.py                 # Flask backend + NLP + matching logic
├── faq_data.json          # FAQ dataset (edit this to change topic!)
├── requirements.txt
├── templates/
│   └── index.html         # Chat UI page
└── static/
    ├── style.css           # Chat UI styling
    └── script.js           # Sends/receives messages via fetch()
```

---

## ▶️ How to run it locally (step by step)

1. **Install Python 3.9+** if you don't have it already.

2. **Open a terminal in the `FAQChatbot` folder** and create a virtual
   environment (recommended but optional):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```
   The first run will download some small NLTK data files automatically
   (this is normal and only happens once).

5. **Open your browser** and go to:
   ```
   http://127.0.0.1:5000
   ```
   You should see the chat window. Try asking things like:
   - "How many tasks do I need to complete?"
   - "Do I need to upload code to GitHub?"
   - "What is cosine similarity?"

---

## ✏️ How to customize it for a different topic

This chatbot isn't hard-coded to internships — to reuse it for any
other topic (a product FAQ, a college FAQ, etc.), just replace the
contents of `faq_data.json` with your own question/answer pairs in the
same format:
```json
[
  { "question": "...", "answer": "..." }
]
```
Nothing else in the code needs to change.

---

## 🚀 Deploying it (so it works from your GitHub Pages / LinkedIn post)

**Important:** unlike LinguaSwift, this project has a **Python backend**
(Flask), so it can't run on GitHub Pages (which only hosts static
HTML/CSS/JS). To make it live, deploy it on a free Python-friendly host
instead, for example:
- **Render.com** (free tier, easiest — connect your GitHub repo, set
  the start command to `python app.py`, done)
- **PythonAnywhere** (free tier for small Flask apps)
- **Railway.app**

You can still push the source code to GitHub as instructed
(`CodeAlpha_FAQChatbot` repo) — the GitHub repo link is what you post on
LinkedIn, and you can additionally share the live Render/PythonAnywhere
link if you want people to try it.

---

## 📌 Task checklist (matches the internship requirements)

- [x] Collect FAQs related to a topic (CodeAlpha internship)
- [x] Preprocess text using NLP libraries (NLTK: tokenize, remove
      stopwords, lemmatize)
- [x] Match user questions to FAQs using cosine similarity
- [x] Display the best matching answer as a chatbot response
- [x] (Optional) Simple chat UI for user interaction
