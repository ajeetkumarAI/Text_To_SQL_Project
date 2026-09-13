import streamlit as st
from text_to_sql import question_to_sql
from database import execute_query

st.set_page_config(page_title="Text to SQL Assistant", page_icon="🤖", layout="centered")

# Custom CSS for enhanced look and feel
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #c7f9e5 0%, #e0e7ff 100%);
    }
    .main {
        background: transparent;
        border-radius: 18px;
        padding: 0;
        box-shadow: none;
        margin-top: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1rem; /* Reduced from 1.2rem to 1rem */
        padding: 0.5rem;
        border-radius: 8px;
        border: 1.5px solid #10b981;
        background-color: #f0fdfa;
        color: #2563eb;
        font-weight: 500;
    }
    .stTextInput>div>div>input::placeholder {
        color: #64748b;
        opacity: 1;
    }
    .stButton>button {
        font-size: 1.1rem;
        background: linear-gradient(90deg, #10b981 60%, #38bdf8 100%);
        color: white;
        padding: 0.4rem 2.5rem;    /* More height for better look, more width */
        border: none;
        border-radius: 6px;        /* Slightly rounded corners */
        transition: background 0.3s;
        box-shadow: 0 2px 8px 0 rgba(16, 185, 129, 0.10);
        width: 100%;               /* Make button fill the column */
        text-align: center;        /* Center the text horizontally */
        display: flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;       /* Prevent text wrapping */
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #059669 60%, #0ea5e9 100%);
        color: #fff;
    }
    .stMarkdown {
        font-size: 1.1rem;
    }
    .company-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #2563eb;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 0.5rem;
        border-bottom: none;
    }
    .stDataFrame {
        background-color: #f0fdfa;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with company info (with AI/text-to-SQL themed image)
st.sidebar.markdown(
    """
    <div style='text-align:center; margin-bottom:1rem;'>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
             alt="AI Text to SQL Agent" style="width:90%; max-width:180px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.07); margin-bottom:0.7rem;">
    </div>
    <h3 style='color:#2563eb;'>Northstar Data Studio</h3>
    <p style='color:#64748b;'>Empowering business intelligence with AI-driven automation.</p>
    <hr>
    <p style='font-size:0.95rem;'>Local text-to-SQL workspace</p>
    """,
    unsafe_allow_html=True,
)

# Main header and subtitle
st.markdown('<div class="company-header">Northstar Data Studio</div>', unsafe_allow_html=True)
st.markdown(
    "<div style='font-size:2rem; color:#64748b; text-align:center; margin-bottom:1.2rem; border-bottom:none;'>🤖 Text to SQL Assistant</div>",
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.write(
        "Ask a business question in natural language. "
        "The assistant will generate the SQL and show the results."
    )

    # Use session state to trigger query on Enter or button
    def submit_query():
        st.session_state["submit"] = True

    # Use a separate key for the text input value
    question = st.text_input(
        "Enter your question:",
        value=st.session_state.get("question_value", ""),
        key="question_value",
        on_change=submit_query
    )

    # Button aligned to the right below the text input
    col1, col2 = st.columns([6, 1])
    with col2:
        button_pressed = st.button("Get Answer", use_container_width=True)
    submit = button_pressed or st.session_state.get("submit", False)

    if submit and st.session_state.get("question_value", "").strip():
        greetings = ["hi", "hello", "hey"]
        user_question = st.session_state["question_value"].strip()
        if user_question.lower() in greetings:
            st.success("Hello, welcome to Northstar Data Studio! 👋\n\nHow can I assist you today?")
        else:
            with st.spinner("Generating SQL and fetching results..."):
                try:
                    sql_query = question_to_sql(user_question)
                    st.subheader("Generated SQL")
                    st.code(sql_query, language="sql")

                    results = execute_query(sql_query)
                    st.subheader("Query Results")
                    # Handle DataFrame and other result types
                    if hasattr(results, "empty"):
                        if not results.empty:
                            st.dataframe(results)
                        else:
                            st.info("No results found.")
                    elif results:
                        st.dataframe(results)
                    else:
                        st.info("No results found.")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.session_state["submit"] = False
        # Do NOT clear st.session_state["question_value"] here to avoid StreamlitAPIException
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
