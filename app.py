from streamlit_mic_recorder import mic_recorder
from voice.speaker import speak
import io
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from tools.web_search import web_search
from tools.router import use_tool, route_query
from core.router_llm import ai_route
from agents.manager import handle_local_request
from agents.chat_agent import chat_reply
from agents.pdf_agent import pdf_context
from database.chat_history import (
    init_db,
    create_conversation,
    save_message,
    load_messages,
    get_conversations,
    clear_database
)
import os

# Load API Key
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="wide"
)
init_db()

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


# Sidebar - Nova Memory
st.sidebar.title("🧠 Nova Memory")
st.sidebar.divider()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if st.sidebar.button("➕ New Chat", key="new_chat_button"):
    st.session_state.conversation_id = create_conversation()
    st.session_state.messages = []
    st.rerun()

# Load messages for the selected conversation
if "messages" not in st.session_state:
    st.session_state.messages = load_messages(
        st.session_state.conversation_id
    )
st.sidebar.subheader("💬 Conversations")

conversations = get_conversations()


st.title("🤖 Nova")
st.caption("Your Personal AI Assistant")

audio = mic_recorder(
    start_prompt="🎤 Start Talking",
    stop_prompt="⏹ Stop",
    key="main_mic_recorder"
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
    type=["pdf"],
    key="pdf_uploader_main"
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
st.sidebar.divider()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if st.sidebar.button("➕ New Chat"):
    st.session_state.conversation_id = create_conversation()
    st.session_state.messages = []
    st.rerun()

st.sidebar.subheader("💬 Conversations")

conversations = get_conversations()

for cid, title in conversations:
    if st.sidebar.button(title, key=f"chat_{cid}"):
        st.session_state.conversation_id = cid
        st.session_state.messages = load_messages(cid)
        st.rerun()
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

# 🔊 Voice Settings
st.sidebar.divider()
st.sidebar.subheader("🔊 Voice Settings")

voice_reply = st.sidebar.toggle(
    "Speak responses",
    value=False
)
# Clear only the current chat
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Delete all saved chat history from SQLite
if st.sidebar.button("🗑️ Delete Saved History"):
    clear_database()
    st.session_state.messages = []
    st.rerun()

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
    save_message(
        st.session_state.conversation_id,
        "user",
        prompt
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
           
            route, local_reply = handle_local_request(
                prompt,
                memory,
                pdf_text
            )
            if local_reply:
                st.caption(f"🧭 Agent: {route.title()} Agent")
                st.markdown(local_reply)

                answer = local_reply
            else:
                st.caption("🧭 Agent: Chat Agent")

                pdf_info = pdf_context(pdf_text)

                if pdf_info:
                    system_prompt += "\n\n" + pdf_info

                answer = chat_reply(
                    st.session_state.messages,
                    system_prompt
                )

            st.markdown(answer)

            # Web Search
            if route == "web":
                with st.spinner("🌐 Searching the web..."):
                    live_info = web_search(prompt)

                system_prompt += f"\n\nUse these live web search results:\n{live_info}"

            # Local Tools
            elif route == "tool":
                tool_result = use_tool(prompt)

                st.markdown(tool_result)
                st.session_state.messages.append(
                    {"role": "assistant", "content": tool_result}
                )

                st.stop()
                st.caption(f"🧭 Route: {route}")
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
            if voice_reply:
                audio_path = speak(answer)
                st.audio(audio_path, format="audio/mp3", autoplay=True)
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    save_message(
        st.session_state.conversation_id,
        "assistant",
        answer
    )