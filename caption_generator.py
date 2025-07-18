import streamlit as st
import requests
import os

# Load Groq API key from Streamlit secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)

if not GROQ_API_KEY:
    st.error("⚠️ API key not found. Please set 'GROQ_API_KEY' in Streamlit secrets.")
    st.stop()

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

st.set_page_config(page_title="Instagram Caption Generator", page_icon="📸")
st.title("📸 AI Instagram Caption Generator")
st.write("Describe your post, pick a tone, and get AI-generated captions instantly.")

post = st.text_area("📝 Describe your Instagram post", placeholder="E.g. A sunset view from the hills...")
tone = st.selectbox("🎨 Choose a tone", ["Funny", "Poetic", "Professional", "Trendy"])

if st.button("✨ Generate Caption"):
    if not post:
        st.warning("Please describe your post first.")
    else:
        with st.spinner("Generating..."):
            prompt = f"""You are a creative Instagram caption writer.

Write a short Instagram caption in a {tone.lower()} tone for the following description:
"{post}"

Only return the caption. No hashtags unless they fit naturally."""

            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 100
            }

            try:
                res = requests.post(GROQ_API_URL, headers=headers, json=payload)
                res.raise_for_status()
                caption = res.json()['choices'][0]['message']['content'].strip()
                st.success("📣 Generated Caption:")
                st.code(caption, language='markdown')

            except Exception as e:
                st.error("❌ Something went wrong:")
                st.error(str(e))
