from streamlit_mic_recorder import mic_recorder
from voice.speaker import speak
import io
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from tools.web_search import web_search
import os

# Load API Key
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="wide"
)
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

st.title("🤖 Nova")
st.caption("Your Personal AI Assistant")

audio = mic_recorder(
    start_prompt="🎤 Start Talking",
    stop_prompt="⏹ Stop",
    key="mic"
)

voice_prompt = None

if audio and audio.get("bytes"):
    with st.spinner("🎤 Transcribing..."):
        audio_file = io.BytesIO(audio["bytes"])
        audio_file.name = "voice.wav"

        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=audio_file
        )

        voice_prompt = transcript.text
        st.success(f"You said: {voice_prompt}")

st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
</style>
""", unsafe_allow_html=True)
from pypdf import PdfReader

uploaded_file = st.file_uploader(
    "📄 Upload a PDF",
    type=["pdf"]
)
if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    st.session_state.pdf_text = text
    st.success("PDF uploaded successfully!")

pdf_text = st.session_state.pdf_text

# Sidebar - Nova Memory
st.sidebar.title("🧠 Nova Memory")

try:
    import json

    with open("memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)

    st.sidebar.write(f"**Name:** {memory.get('name', '—')}")
    st.sidebar.write(f"**City:** {memory.get('city', '—')}")
    st.sidebar.write(f"**College:** {memory.get('college', '—')}")
    st.sidebar.write(f"**Favorite Language:** {memory.get('favorite_language', '—')}")

except:
    st.sidebar.write("No memory yet.")


# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
typed_prompt = st.chat_input("Ask Nova anything...")

prompt = voice_prompt if voice_prompt else typed_prompt

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Nova is thinking..."):

            # Build the system prompt
            system_prompt = "You are Nova, a helpful personal AI assistant."

            # Use uploaded PDF if available
            if pdf_text:
                system_prompt += f"\n\nThe user uploaded this PDF:\n{pdf_text[:5000]}"

            # Use web search when needed
            live_info = ""

            search_words = [
                "today",
                "latest",
                "news",
                "weather",
                "score",
                "price",
                "current"
            ]

            if any(word in prompt.lower() for word in search_words):
                with st.spinner("🌐 Searching the web..."):
                    live_info = web_search(prompt)

                system_prompt += (
                    "\n\nUse these live web search results:\n"
                    f"{live_info}"
                )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    *st.session_state.messages
                ]
            )
            answer = response.choices[0].message.content

            st.markdown(answer)
            audio_path = speak(answer)

            st.audio(audio_path, format="audio/mp3", autoplay=True)
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )