import streamlit as st
from datetime import datetime

from src.rag import AcademicRAG
from src.llm import GeminiLLM
from src.config import PDF_PATH, TOP_K

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="EPCET Academic Regulation Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS (Fluid & Modern)
# =========================================================
st.markdown("""
<style>
    /* Global Fluidity & Spacing */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        max-width: 95% !important;
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
    }
    
    /* Hide Streamlit Top Decoration */
    [data-testid="stDecoration"] {
        display: none;
    }

    /* Modern Top Header (Hero) */
    .hero-container {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-text h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .hero-text p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .hero-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #edf2f7;
    }
    .sidebar-header {
        text-align: center;
        padding: 1rem 0;
    }
    .sidebar-header h2 {
        color: #123b66;
        margin: 0;
        font-size: 1.5rem;
    }
    .sidebar-header p {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    .status-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: #ecfdf5;
        color: #059669;
        padding: 8px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    .status-dot {
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 3px #a7f3d0;
    }

    /* Chat Messages Styling */
    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    /* User Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
    }
    /* Assistant Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #123b66;
    }

    /* Buttons Fluidity */
    .stButton button {
        width: 100%;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        color: #334155 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        border-color: #123b66 !important;
        color: #123b66 !important;
        background: #f8fafc !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD SYSTEM
# =========================================================
@st.cache_resource
def load_system():
    rag = AcademicRAG()
    llm = GeminiLLM()
    return rag, llm

rag, llm = load_system()


# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h2>🎓 EPCET</h2>
            <p>Regulation Assistant</p>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div> System Online
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("**⚡ Quick Actions**")
    
    quick_qs = [
        "What are the attendance requirements?",
        "How is CGPA calculated?",
        "What are the passing requirements?",
        "What are the rules for examinations?",
        "What are the eligibility requirements for promotion?"
    ]
    
    for q in quick_qs:
        if st.button(q):
            st.session_state.pending_question = q

    st.divider()
    
    st.markdown("**📄 Knowledge Base**")
    st.info(f"Connected to:\n**{getattr(PDF_PATH, 'name', 'Academic Regulations')}**", icon="📁")
    
    if st.button("🗑️ Clear Conversation", type="primary"):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


# =========================================================
# MAIN LAYOUT
# =========================================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-text">
            <h1>Academic Regulations Assistant</h1>
            <p>Ask anything about EPCET guidelines, grading, and policies.</p>
        </div>
        <div class="hero-badge">v2.0 Fluid Streaming</div>
    </div>
""", unsafe_allow_html=True)

# Welcome Screen
if not st.session_state.messages and not st.session_state.pending_question:
    st.markdown("### 👋 Welcome! How can I help you today?")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Try asking about:**\n* Attendance limits & condonation\n* Promotion rules to next semester", icon="💡")
    with col2:
        st.success("**Or ask about:**\n* Internal vs External marks\n* CGPA / SGPA conversion formulas", icon="📈")

# Render existing chat history
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🎓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        
        if message.get("sources"):
            st.caption("📚 References:")
            for i, source in enumerate(message["sources"], 1):
                sec_num = source.get("section_number", "N/A")
                sec_title = source.get("section_title", "General")
                with st.expander(f"Reference {i}: Section {sec_num} - {sec_title}"):
                    st.write(source.get("text", ""))

# Input box captures query
user_input = st.chat_input("Type your question here (e.g., 'What is the minimum attendance?')...")
if user_input:
    st.session_state.pending_question = user_input


# =========================================================
# PROCESS NEW QUESTION (Streaming Logic)
# =========================================================
if st.session_state.pending_question:
    q = st.session_state.pending_question
    
    # 1. Immediately append and display the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": q,
        "time": datetime.now().strftime("%H:%M")
    })
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(q)

    # 2. Display the assistant's message container and start streaming
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Searching regulations..."):
            try:
                # Retrieve context from ChromaDB
                results = rag.search(q, top_k=TOP_K)
                documents = results.get("documents", [[]])[0]
                metadatas = results.get("metadatas", [[]])[0]
                
                if not documents:
                    answer = "I couldn't find this information in the academic regulations."
                    st.markdown(answer)
                    sources = []
                else:
                    # Construct context
                    context_parts = [
                        f"[Section {m.get('section_number', 'N/A')} - {m.get('section_title', 'Regs')}]\n{d}" 
                        for d, m in zip(documents, metadatas)
                    ]
                    context = "\n\n".join(context_parts)
                    
                    # Call LLM and stream the generator output to the UI instantly
                    stream_generator = llm.ask(context, q)
                    answer = st.write_stream(stream_generator)
                    
                    # Prepare sources for rendering
                    sources = [{"text": d, **m} for d, m in zip(documents, metadatas)]
                    
                    # Display the sources below the freshly generated answer
                    if sources:
                        st.caption("📚 References:")
                        for i, source in enumerate(sources, 1):
                            sec_num = source.get("section_number", "N/A")
                            sec_title = source.get("section_title", "General")
                            with st.expander(f"Reference {i}: Section {sec_num} - {sec_title}"):
                                st.write(source.get("text", ""))

            except Exception as e:
                answer = f"Sorry, I encountered an error: {str(e)}"
                st.markdown(answer)
                sources = []

    # 3. Save the completely generated message and sources to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "time": datetime.now().strftime("%H:%M")
    })

    # Clear pending question to finish the loop
    st.session_state.pending_question = None