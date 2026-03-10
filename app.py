import streamlit as st
import requests
import threading
import time
from pathlib import Path

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Blood Test Report Analyser", page_icon="🩸", layout="centered")

# Initialize session state for API config
if "api_configured" not in st.session_state:
    st.session_state.api_configured = False
    st.session_state.gemini_api_key = ""
    st.session_state.search_web_key = ""
    st.session_state.search_engine_id = ""

# --- API Configuration Screen (shown until Start is clicked) ---
if not st.session_state.api_configured:
    st.title("Blood Test Report Analyser")
    st.subheader("API Configuration")
    st.markdown("Enter your API keys to get started.")

    gemini_api_key = st.text_input("Gemini API Key", type="password", help="Google Gemini API key")
    search_web_key = st.text_input("Search Web API Key", type="password", help="Google Custom Search API key")
    search_engine_id = st.text_input("Search Engine ID", help="Google Custom Search Engine ID")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        start_clicked = st.button("Start", type="primary", use_container_width=True)

    if start_clicked:
        if not all([gemini_api_key, search_web_key, search_engine_id]):
            st.error("Please fill in all three API keys.")
        else:
            st.session_state.gemini_api_key = gemini_api_key
            st.session_state.search_web_key = search_web_key
            st.session_state.search_engine_id = search_engine_id
            st.session_state.api_configured = True
            st.rerun()

    st.stop()

# --- Main Screen (only shown after API keys are configured) ---
st.title("Blood Test Report Analyser")
st.markdown("Upload a blood test PDF report to get analysis, relevant articles, and health recommendations.")

# Show a reset button in sidebar to reconfigure keys
if st.sidebar.button("Reconfigure API Keys"):
    st.session_state.api_configured = False
    st.rerun()

st.sidebar.success("API keys configured.")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload Blood Test Report (PDF)", type=["pdf"])

if uploaded_file:
    input_filename = Path(uploaded_file.name).stem
    output_filename = f"{input_filename}-recommendation.pdf"

    if st.button("Analyse Report", type="primary", use_container_width=True):
        progress_bar = st.progress(0, text="Uploading PDF to backend...")
        progress_messages = [
            (10, "Uploading PDF to backend..."),
            (20, "Extracting text from PDF..."),
            (30, "Initializing AI agents..."),
            (40, "Analysing blood test report..."),
            (50, "Searching for relevant articles..."),
            (60, "Generating health recommendations..."),
            (70, "Compiling results..."),
            (80, "Almost done..."),
        ]

        # Capture values before threading (st.session_state not accessible from threads)
        api_keys = {
            "gemini_api_key": st.session_state.gemini_api_key,
            "search_web_key": st.session_state.search_web_key,
            "search_engine_id": st.session_state.search_engine_id,
        }
        file_name = uploaded_file.name
        file_bytes = uploaded_file.getvalue()

        # Run backend request in a thread so we can animate the progress bar
        result_holder = {"response": None, "error": None, "done": False}

        def call_backend():
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/analyse",
                    files={"file": (file_name, file_bytes, "application/pdf")},
                    data=api_keys,
                    timeout=300,
                )
                result_holder["response"] = resp
            except Exception as e:
                result_holder["error"] = e
            finally:
                result_holder["done"] = True

        thread = threading.Thread(target=call_backend)
        thread.start()

        # Animate progress bar while backend is working
        step = 0
        while not result_holder["done"]:
            if step < len(progress_messages):
                pct, msg = progress_messages[step]
                progress_bar.progress(pct, text=msg)
                step += 1
            time.sleep(3)

        thread.join()

        # Handle errors from the thread
        if result_holder["error"] is not None:
            progress_bar.empty()
            err = result_holder["error"]
            if isinstance(err, requests.exceptions.ConnectionError):
                st.error("Cannot connect to the backend server. Make sure it is running (use ./start.sh).")
            elif isinstance(err, requests.exceptions.Timeout):
                st.error("The request timed out. The report may be too large or the AI agents are taking too long.")
            else:
                st.error(f"An error occurred: {str(err)}")
            st.stop()

        response = result_holder["response"]

        try:
            progress_bar.progress(85, text="Processing complete. Fetching results...")

            if response.status_code != 200:
                progress_bar.empty()
                detail = response.json().get("detail", "Unknown error from backend.")
                st.error(f"Backend error: {detail}")
                st.stop()

            result = response.json()
            analysis_text = result["analysis"]
            articles_text = result["articles"]
            recommendations_text = result["recommendations"]
            pdf_path = result["pdf_path"]
            out_filename = result["output_filename"]

            progress_bar.progress(90, text="Fetching generated PDF...")
            pdf_response = requests.get(
                f"{BACKEND_URL}/download",
                params={"path": pdf_path, "filename": out_filename},
                timeout=30,
            )

            if pdf_response.status_code != 200:
                pdf_bytes = None
            else:
                pdf_bytes = pdf_response.content

            progress_bar.progress(100, text="Analysis complete!")

        except Exception as e:
            progress_bar.empty()
            st.error(f"An error occurred: {str(e)}")
            st.stop()

        # Display results
        st.subheader("Blood Test Analysis")
        st.markdown(analysis_text)

        st.subheader("Relevant Articles")
        st.markdown(articles_text)

        st.subheader("Health Recommendations")
        st.markdown(recommendations_text)

        # Download button
        if pdf_bytes:
            st.download_button(
                label=f"Download Report ({output_filename})",
                data=pdf_bytes,
                file_name=output_filename,
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
