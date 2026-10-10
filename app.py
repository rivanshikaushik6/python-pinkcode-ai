
import os
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -------------------- SETUP --------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="PinkCode AI",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- PINK GIRLY UI --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --pink: #e75480;
    --deep-pink: #c93669;
    --soft-pink: #fff0f5;
    --pale-pink: #fff8fb;
    --rose: #f7c5d5;
    --ink: #54283d;
}

/* Main application backgrounds */
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #fff0f6 !important;
    background-color: #fff0f6 !important;
    color: #54283d !important;
    font-family: 'DM Sans', sans-serif;
}

/* Main page gradient */
.stApp {
    background:
        radial-gradient(ellipse at top left, #ffe0eb 0%, transparent 35%),
        linear-gradient(135deg, #fff8fb 0%, #fff0f6 55%, #ffeaf2 100%) !important;
}

/* Header */
[data-testid="stHeader"] {
    background: #fff5f9 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffe4ee, #fff3f8 65%, #ffeaf2) !important;
    border-right: 1px solid #f5c5d6;
}

[data-testid="stSidebar"] * {
    color: #642d48;
}

/* Headings */
h1, h2, h3 {
    color: #a83260 !important;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.7rem !important;
    letter-spacing: -1px;
}

/* General readable text */
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: #54283d;
}

/* Hero banner */
.pink-hero {
    background: linear-gradient(120deg, #f8c7d9, #ffe8f0 55%, #fff7fa);
    border: 1px solid #f1bed1;
    padding: 25px 28px;
    border-radius: 24px;
    margin: 10px 0 24px 0;
    box-shadow: 0 8px 25px rgba(190, 83, 124, 0.09);
}

.pink-hero h2 {
    font-family: 'Playfair Display', serif;
    color: #9e315c !important;
    margin: 0 0 8px 0;
}

.pink-hero p {
    color: #754057 !important;
    margin: 0;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #f4ccda;
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 5px 18px rgba(190, 83, 124, 0.06);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #54283d !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #e75480, #cf3970) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    border-radius: 14px;
    padding: 0.65rem 1.1rem;
    font-weight: 700;
    box-shadow: 0 5px 12px rgba(207, 57, 112, 0.18);
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #cf3970, #b72b5c) !important;
    transform: translateY(-2px);
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #54283d !important;
    -webkit-text-fill-color: #54283d !important;
    border: 1px solid #edbfd0 !important;
    border-radius: 12px;
}

/* Dropdowns */
.stSelectbox [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #edbfd0 !important;
    border-radius: 12px;
}

.stSelectbox div,
.stSelectbox span,
[data-baseweb="select"] * {
    color: #54283d !important;
}

/* Dropdown options */
[role="option"] {
    background-color: #fff8fb !important;
    color: #54283d !important;
}

/* ---------------- CHAT AREA BACKGROUND FIX ---------------- */

/* Force Streamlit's bottom containers to use pink */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div,
[data-testid="stBottom"] form,
[data-testid="stBottom"] > div > div {
    background: #fff0f6 !important;
    background-color: #fff0f6 !important;
}

/* Chat input container */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] form {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1.5px solid #e75480 !important;
    border-radius: 18px !important;
    box-shadow: 0 5px 20px rgba(231, 84, 128, 0.12) !important;
}

/* Typed text and placeholder */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea::placeholder {
    color: #54283d !important;
    -webkit-text-fill-color: #54283d !important;
    opacity: 1 !important;
    background: transparent !important;
    caret-color: #e75480 !important;
}

/* Pink send button */
[data-testid="stChatInput"] button {
    background: #e75480 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-radius: 12px !important;
}

/* Remove dark pseudo-element overlays */
[data-testid="stBottom"]::before,
[data-testid="stBottom"]::after,
[data-testid="stBottomBlockContainer"]::before,
[data-testid="stBottomBlockContainer"]::after {
    background: #fff0f6 !important;
    background-color: #fff0f6 !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid #f1c4d4;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.8) !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.85) !important;
    padding: 16px;
    border: 1px solid #f2c8d7;
    border-radius: 16px;
}

/* Dividers */
hr {
    border-color: #f2c8d7;
}

/* Code blocks */
.stCode,
.stCode pre,
.stCode code,
pre,
code {
    color: #54283d;
}

/* Hide Streamlit menu and footer */
#MainMenu,
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# -------------------- GEMINI CONNECTION --------------------

if not api_key:
    st.error("🎀 API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# -------------------- SESSION STATE --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("# 🎀 PinkCode AI")
    st.caption("your cute little coding companion")
    st.divider()

    st.markdown("### ✨ Your workspace")

    mode = st.selectbox(
        "Choose your coding tool",
        [
            "General Coding Assistant",
            "Debug My Code",
            "Generate Code",
            "Explain Code Line by Line",
        ],
    )

    language = None

    if mode == "Generate Code":
        language = st.selectbox(
            "Programming language",
            [
                "Python",
                "Java",
                "C",
                "C++",
                "JavaScript",
                "HTML and CSS",
                "SQL",
                "Go",
                "Other / Specify in prompt",
            ],
        )

    st.divider()
    st.markdown("### 💗 Session")
    st.metric(
        "Messages in this session",
        len(st.session_state.messages),
    )

    if st.button("🗑️ Clear current chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Made with 💗, Python & Gemini")

# -------------------- MAIN PAGE --------------------

st.markdown("""
<div class="pink-hero">
    <h2>Hey, girlie! Ready to code? 🎀</h2>
    <p>Your personal AI coding bestie — debug errors, create projects,
    generate code, and understand every line.</p>
</div>
""", unsafe_allow_html=True)

st.title("PinkCode AI")
st.caption("✨ Think it. Code it. Debug it. Own it.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**🐞 Debug**")
    st.caption("Fix coding errors")

with col2:
    st.markdown("**💻 Generate**")
    st.caption("Create code")

with col3:
    st.markdown("**📚 Explain**")
    st.caption("Learn line by line")

with col4:
    st.markdown("**💬 Chat**")
    st.caption("Ask anything coding")

st.divider()

# -------------------- DISPLAY CHAT HISTORY --------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- CHAT INPUT --------------------

prompt = st.chat_input("Ask your coding bestie anything... 💗")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Instructions for the selected mode
    if mode == "Debug My Code":
        instructions = """
        You are an expert code debugger.
        Identify bugs and explain why they happen.
        Provide corrected code in a code block.
        Explain the fixes in beginner-friendly language.
        Never claim to execute code unless it was actually executed.
        If code is missing, ask the user to paste it.
        """

    elif mode == "Generate Code":
        instructions = f"""
        You are an expert programming assistant.
        Generate readable, complete code in {language}.
        Put the complete code in a fenced Markdown code block.
        Explain how it works in simple language.
        Include example input and output when useful.
        If the user explicitly requests another language, follow
        the user's request.
        """

    elif mode == "Explain Code Line by Line":
        instructions = """
        You are a patient programming tutor.
        Explain the user's code line by line in simple language.
        Describe important variables, functions, and logic.
        Use examples when helpful.
        If code is missing, ask the user to paste it.
        """

    else:
        instructions = """
        You are a helpful AI coding assistant.
        Write readable code and explain it simply.
        Help users solve programming problems step by step.
        Be friendly, encouraging, and beginner-friendly.
        """

    # Build conversation history for Gemini
    history = []

    for message in st.session_state.messages:
        history.append({
            "role": (
                "user" if message["role"] == "user" else "model"
            ),
            "parts": [{"text": message["content"]}],
        })

    # Ask Gemini
    with st.chat_message("assistant"):
        with st.spinner("✨ Your coding bestie is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=history,
                    config={"system_instruction": instructions},
                )

                answer = (
                    response.text
                    or "No text response returned. Please try again."
                )

                st.markdown(answer)

                # Download generated code
                if mode == "Generate Code":
                    extensions = {
                        "Python": "generated_code.py",
                        "Java": "Main.java",
                        "C": "generated_code.c",
                        "C++": "generated_code.cpp",
                        "JavaScript": "generated_code.js",
                        "HTML and CSS": "index.html",
                        "SQL": "generated_code.sql",
                        "Go": "main.go",
                        "Other / Specify in prompt": "generated_code.txt",
                    }

                    filename = extensions.get(
                        language, "generated_code.txt"
                    )

                    code_blocks = re.findall(
                        r"```(?:[a-zA-Z0-9_+#.-]+)?[ \t]*\n(.*?)```",
                        answer,
                        re.DOTALL,
                    )

                    if code_blocks:
                        code_to_download = "\n\n".join(
                            block.strip() for block in code_blocks
                        )

                        st.download_button(
                            label="🎀 Download your code",
                            data=code_to_download,
                            file_name=filename,
                            mime="text/plain",
                        )

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(
                    "Oops! The AI request failed. Check your internet, "
                    "API key, model availability, and API quota."
                )
                st.code(str(error))

                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"] == "user"
                ):
                    st.session_state.messages.pop()
