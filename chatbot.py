import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Predefined intents & responses

career_data = {
    "data_scientist": {
        "questions": [
            "how to become data scientist",
            "data scientist career",
            "roadmap for data scientist"
        ],
        "response": (
            "To become a Data Scientist:\n"
            "1. Learn Python\n"
            "2. Study Statistics\n"
            "3. Learn Machine Learning\n"
            "4. Work on Projects\n"
            "5. Practice SQL & Data Analysis"
        )
    },
    "web_developer": {
        "questions": [
            "how to become web developer",
            "web development career",
            "roadmap for web developer"
        ],
        "response": (
            "To become a Web Developer:\n"
            "1. Learn HTML, CSS\n"
            "2. Learn JavaScript\n"
            "3. Learn React\n"
            "4. Backend with Python (Django/Flask)\n"
            "5. Build projects"
        )
    },
    "python_developer": {
        "questions": [
            "how to become python developer",
            "python career",
            "roadmap for python developer"
        ],
        "response": (
            "To become a Python Developer:\n"
            "1. Core Python\n"
            "2. OOP Concepts\n"
            "3. Flask/Django\n"
            "4. SQL & APIs\n"
            "5. Real-world projects"
        )
    }
}


# NLP helper functions

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z ]", "", text)
    return text


def get_best_response(user_input):
    user_input = clean_text(user_input)

    all_questions = []
    responses = []

    for intent in career_data.values():
        for q in intent["questions"]:
            all_questions.append(q)
            responses.append(intent["response"])

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_questions + [user_input])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return responses[best_match_index]
    else:
        return "Sorry, I didn't understand. Please ask about a career roadmap."


# Streamlit UI

def show_chatbot():
    st.title("🤖 Career Guidance Chatbot ")
    st.write("Ask career-related questions ")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:", placeholder="How to become a data scientist?")

    if st.button("Send"):
        if user_input.strip() != "":
            response = get_best_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
