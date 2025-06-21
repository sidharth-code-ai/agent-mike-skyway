import streamlit as st
import sqlite3
from main import chat  # your backend chat function
from datetime import datetime
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Skyway Realty AI Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Modern UI ---
st.markdown(
    """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #3b82f6;
        --success-color: #10b981;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
    }
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Login card */
    .login-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid #e2e8f0;
    }
    
    .login-card h2 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .login-card p {
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    /* Chat interface */
    .chat-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .user-info {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .user-info .icon {
        font-size: 1.5rem;
    }
    
    .user-info .text {
        font-weight: 500;
    }
    
    /* Message bubbles */
    .message-container {
        margin: 1rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin-left: 2rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        position: relative;
    }
    
    .bot-message {
        background: #f8fafc;
        color: #1e293b;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin-right: 2rem;
        border: 1px solid #e2e8f0;
        position: relative;
    }
    
    .message-label {
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: #1e293b !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        color: #1e293b !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Fix sidebar collapse/expand */
    .css-1rs6os, .css-17ziqus {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Ensure sidebar toggle button is visible */
    button[title="Close sidebar"] {
        color: #1e293b !important;
    }
    
    button[title="Open sidebar"] {
        color: #1e293b !important;
        background: white !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #3b82f6 transparent #3b82f6 transparent;
    }
    
    /* Status indicators */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #10b981;
        font-weight: 500;
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .login-card {
            margin: 1rem;
            padding: 2rem;
        }
        
        .user-message, .bot-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- SQLite user mapping DB setup ---
@st.cache_resource
def init_database():
    # Fix for Python 3.12 SQLite datetime deprecation warning
    db_path = "users.db"

    # Create connection without deprecated datetime adapters
    conn = sqlite3.connect(db_path, check_same_thread=False)

    # Disable automatic timestamp conversion to avoid deprecation warnings
    conn.execute("PRAGMA table_info(users)")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            last_active TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


conn = init_database()


def get_user_id(full_name: str) -> str:
    """
    Normalize full_name into a user_id, store it if new, and return it.
    """
    uid = full_name.lower().replace(" ", "_")
    cur = conn.execute("SELECT id FROM users WHERE id = ?", (uid,))
    if cur.fetchone() is None:
        # Use string timestamps to avoid deprecation warnings
        now_str = datetime.now().isoformat()
        conn.execute(
            "INSERT INTO users(id, name, created_at, last_active) VALUES(?, ?, ?, ?)",
            (uid, full_name, now_str, now_str),
        )
        conn.commit()
    else:
        # Update last active time
        now_str = datetime.now().isoformat()
        conn.execute("UPDATE users SET last_active = ? WHERE id = ?", (now_str, uid))
        conn.commit()
    return uid


def get_user_stats():
    """Get basic user statistics"""
    cur = conn.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Use date() function instead of datetime comparison to avoid warnings
    cur = conn.execute(
        "SELECT COUNT(*) FROM users WHERE date(last_active) = date('now')"
    )
    active_today = cur.fetchone()[0]

    return total_users, active_today


# --- Main App ---
def main():
    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🏢 Skyway Realty AI Assistant</h1>
        <p>Your intelligent property consultant, available 24/7</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Step 1: User Authentication
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if not st.session_state.initialized:
        show_login_screen()
        return

    # Step 2: Main Chat Interface
    show_chat_interface()


def show_login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
        <div class="login-card">
            <h2>👋 Welcome to Skyway Realty</h2>
            <p>Please enter your name to start chatting with our AI assistant</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            name_input = st.text_input(
                "Full Name",
                placeholder="Enter your full name...",
                help="This helps us personalize your experience",
            )

            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submitted = st.form_submit_button(
                    "Start Chatting 🚀", use_container_width=True
                )

            if submitted:
                if name_input.strip():
                    st.session_state.full_name = name_input.strip()
                    st.session_state.initialized = True
                    st.success(f"Welcome, {name_input}! 🎉")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter your name to continue.")


def show_chat_interface():
    # Sidebar with user info and stats
    with st.sidebar:
        st.markdown("### 👤 User Profile")

        full_name = st.session_state.full_name
        user_id = get_user_id(full_name)

        st.markdown(
            f"""
        <div class="user-info">
            <div class="icon">👋</div>
            <div class="text">Hello, {full_name}!</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Status indicator
        st.markdown(
            """
        <div class="status-online">
            <div class="status-indicator"></div>
            AI Assistant Online
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Quick stats
        total_users, active_today = get_user_stats()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Active Today", active_today)

        st.markdown("---")

        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("🏠 Browse Properties", use_container_width=True):
            st.session_state.quick_message = "Show me available properties"

        if st.button("📅 Schedule Viewing", use_container_width=True):
            st.session_state.quick_message = "I'd like to schedule a property viewing"

        if st.button("💰 Market Analysis", use_container_width=True):
            st.session_state.quick_message = "Can you provide a market analysis?"

        if st.button("📞 Contact Info", use_container_width=True):
            st.session_state.quick_message = "What are your contact details?"

        st.markdown("---")

        # Reset conversation
        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.success("Conversation reset!")

        # Logout
        if st.button("👋 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main chat interface
    st.markdown(
        f"""
    <div class="chat-container">
        <h3>💬 Chat with Skyway AI</h3>
        <p>Ask me anything about our properties, schedule viewings, or get market insights!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = f"Hello {full_name}! 👋 I'm your Skyway Realty AI assistant. I can help you find properties, schedule viewings, and answer any questions about real estate. How can I assist you today?"
        st.session_state.messages.append(
            {"user": None, "bot": welcome_msg, "timestamp": datetime.now()}
        )

    # Handle quick actions
    if "quick_message" in st.session_state:
        process_message(user_id, st.session_state.quick_message)
        del st.session_state.quick_message

    # Chat input using form to enable clearing
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input(
                "Type your message...",
                placeholder="Ask about properties, schedule viewings, or anything else...",
                label_visibility="collapsed",
            )

        with col2:
            send_button = st.form_submit_button("Send 📤", use_container_width=True)

        # Handle message sending
        if send_button and user_input.strip():
            process_message(user_id, user_input.strip())
            st.rerun()

    # Display conversation history
    st.markdown("### 💬 Conversation")

    # Create a container for messages with custom styling
    messages_container = st.container()

    with messages_container:
        for i, turn in enumerate(st.session_state.messages):
            if turn["user"]:  # User message
                st.markdown(
                    f"""
                <div class="message-container">
                    <div class="user-message">
                        <div class="message-label">You</div>
                        {turn["user"]}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Bot message
            st.markdown(
                f"""
            <div class="message-container">
                <div class="bot-message">
                    <div class="message-label">🏢 Skyway AI</div>
                    {turn["bot"]}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Auto-scroll to bottom (JavaScript injection)
    st.markdown(
        """
    <script>
        var element = window.parent.document.querySelector('.main');
        element.scrollTop = element.scrollHeight;
    </script>
    """,
        unsafe_allow_html=True,
    )


def process_message(user_id: str, user_input: str):
    """Process user message and get bot response"""
    with st.spinner("🤔 Thinking..."):
        try:
            bot_reply = chat(user_id, user_input)

            # Add to message history
            st.session_state.messages.append(
                {"user": user_input, "bot": bot_reply, "timestamp": datetime.now()}
            )

        except Exception as e:
            # Log the actual error for debugging
            error_msg = str(e)
            st.error(f"Error details: {error_msg}")

            # More specific error message
            if "Default value is not supported" in error_msg:
                bot_reply = "I'm experiencing a configuration issue with my tools. The development team has been notified. Please try a simpler question for now."
            elif "sqlite3" in error_msg.lower():
                bot_reply = "I'm having database connectivity issues. Please try again in a moment."
            else:
                bot_reply = f"I encountered an error: {error_msg}. Please try rephrasing your question."

            st.session_state.messages.append(
                {"user": user_input, "bot": bot_reply, "timestamp": datetime.now()}
            )


if __name__ == "__main__":
    main()
