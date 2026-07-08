"""
================================================================================
 FAQ CHATBOT - app.py
================================================================================
 This is the "brain" of our chatbot. It does 4 things:

   1. Loads a list of FAQ (question, answer) pairs from faq_data.json
   2. Cleans/preprocesses all the FAQ questions using NLTK (tokenizing,
      removing stopwords, and lemmatizing words down to their root form)
   3. Converts all questions into numeric vectors using TF-IDF
   4. When a user types a question, it converts that question into a vector
      too, and uses COSINE SIMILARITY to find which FAQ question is the
      closest match. It then returns that FAQ's answer.

 We use Flask to expose this logic as a small web server with:
   - "/"       -> serves the chat webpage (index.html)
   - "/chat"   -> a POST endpoint the webpage calls with the user's message,
                  which returns the chatbot's reply as JSON
================================================================================
"""

import json
import string

from flask import Flask, render_template, request, jsonify

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------------------------------
# STEP 0: Make sure the NLTK data files we need are downloaded.
# (This only actually downloads the first time you run the app; after that
# it's cached locally, so startup is fast.)
# --------------------------------------------------------------------------
for resource in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource, quiet=True)

lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words("english"))


# --------------------------------------------------------------------------
# STEP 1: Load the FAQ dataset from the JSON file.
# --------------------------------------------------------------------------
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]


# --------------------------------------------------------------------------
# STEP 2: Preprocessing function.
#
# This turns raw text like:
#     "How LONG is the Internship??"
# into a clean list of root words like:
#     ["long", "internship"]
#
# Why do this? Because "How long IS the internship?" and "internship
# duration" mean almost the same thing, but a computer comparing raw text
# wouldn't see that. Preprocessing strips away noise (capitalization,
# punctuation, common filler words like "is"/"the") so the AI can focus on
# the words that actually carry meaning.
# --------------------------------------------------------------------------
def preprocess(text: str) -> str:
    # 2a. Lowercase everything so "Internship" and "internship" match.
    text = text.lower()

    # 2b. Remove punctuation like ? ! , .
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 2c. Tokenize -> split the sentence into individual words.
    tokens = word_tokenize(text)

    # 2d. Remove stopwords (common words like "is", "the", "a") AND
    #     lemmatize each remaining word (reduce it to its root/dictionary
    #     form, e.g. "running" -> "run", "certificates" -> "certificate").
    cleaned_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in STOPWORDS
    ]

    # 2e. Join the cleaned words back into a single string, because that's
    #     the format TfidfVectorizer expects.
    return " ".join(cleaned_tokens)


# --------------------------------------------------------------------------
# STEP 3: Preprocess every FAQ question ONCE at startup, and fit a
# TF-IDF vectorizer on them.
#
# TF-IDF (Term Frequency - Inverse Document Frequency) turns each sentence
# into a list of numbers (a "vector"). Words that are rare across all FAQs
# but appear in a specific question get a HIGH weight (they're more
# distinctive/important), while very common words get a LOW weight.
# --------------------------------------------------------------------------
preprocessed_questions = [preprocess(q) for q in faq_questions]

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(preprocessed_questions)


# --------------------------------------------------------------------------
# STEP 4: The matching function.
#
# Given a user's message, this:
#   a. Preprocesses it the same way as the FAQ questions
#   b. Converts it into a TF-IDF vector using the SAME vectorizer
#      (important: we reuse the vectorizer that was "fit" on the FAQs,
#      we don't fit a new one, otherwise the vectors wouldn't be comparable)
#   c. Computes cosine similarity between the user's vector and every
#      FAQ vector. Cosine similarity gives a score from 0 (completely
#      unrelated) to 1 (identical meaning).
#   d. Picks the FAQ with the highest similarity score.
#   e. If even the best score is too low, it means we don't have a good
#      matching FAQ, so we return a polite fallback message instead of a
#      wrong answer.
# --------------------------------------------------------------------------
SIMILARITY_THRESHOLD = 0.25  # tweak this to make matching stricter/looser

def get_best_answer(user_message: str):
    cleaned = preprocess(user_message)

    # If after cleaning there's nothing left (e.g. user typed just "??"),
    # bail out early with the fallback message.
    if not cleaned.strip():
        return (
            "I'm not sure I understood that. Could you rephrase your question?",
            0.0,
        )

    user_vector = vectorizer.transform([cleaned])

    # cosine_similarity returns a 2D array; we only compare 1 user vector
    # against all FAQ vectors, so we take row [0].
    similarity_scores = cosine_similarity(user_vector, faq_vectors)[0]

    best_index = similarity_scores.argmax()
    best_score = similarity_scores[best_index]

    if best_score < SIMILARITY_THRESHOLD:
        return (
            "I'm not sure about that one. Could you try rephrasing, or ask "
            "something related to the CodeAlpha internship program?",
            float(best_score),
        )

    return faq_answers[best_index], float(best_score)


# --------------------------------------------------------------------------
# STEP 5: Flask web server / API
# --------------------------------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    # Serves the chat UI (templates/index.html)
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    answer, score = get_best_answer(user_message)
    return jsonify({
        "answer": answer,
        "confidence": round(score, 3),
    })


if __name__ == "__main__":
    # debug=True auto-reloads the server when you edit code - handy while
    # developing. Turn it off (or remove it) before deploying anywhere public.
    app.run(debug=True, port=5000)
