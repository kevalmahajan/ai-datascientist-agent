
from nb_agent_backend import generate_agent_stream
from tools.nb_tools import create_noteboook

import streamlit as st
import os
from pathlib import Path
import re

# Set up Streamlit page config
st.set_page_config(page_title="Jupyter Notebook Agent", layout="wide")
st.title("🤖 Notebook Assistant")


# Inject custom CSS for dark mode-friendly output blocks
custom_css = """
<style>
    .output-box {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
        color: #f1f1f1;
        font-family: 'Segoe UI', sans-serif;
    }
    .output-box .label {
        font-weight: 600;
        color: #9cdcfe;
    }
    code {
        background-color: #2d2d2d;
        padding: 3px 6px;
        border-radius: 4px;
        color: #dcdcaa;
        font-size: 0.95em;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Create a persistent temporary directory in the same location as your code
temp_dir = os.path.join(os.getcwd(), "temp_uploads")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Chat output container to hold all messages
chat_container = st.container()

# Sidebar for user input
st.sidebar.header("Task Input")

# File upload
file_upload = st.sidebar.file_uploader(
    "Attach a file (optional)", 
    type=["csv", "txt", "xlsx"]
)

# Task description
user_input = st.sidebar.text_area(
    "Describe your task", 
    height=150, 
    placeholder="e.g. Analyze the uploaded dataset..."
)

# Notebook filename input (without extension)
notebook_name_input = st.sidebar.text_input(
    "Output Notebook Filename (no extension)", 
    placeholder="analysis_report"
)


# Ensure a default name if user doesn't type anything
notebook_filename = (notebook_name_input.strip() or "output") + ".ipynb"


# When user clicks "Start"
if st.sidebar.button("Start"):
    file_path = ""

    create_noteboook(notebook_filename)
    
    # Handle file upload and save in the local temp folder
    if file_upload is not None:
        tmp_file_path = os.path.join(temp_dir, file_upload.name)
        with open(tmp_file_path, "wb") as f:
            f.write(file_upload.getbuffer())
        file_path = Path(tmp_file_path)

    # Display task and file info
    with chat_container:
        st.markdown(f"""<div class="output-box">
            <span class="label">📝 User Task:</span> {user_input}</div>""", unsafe_allow_html=True)
        if file_path:
            st.markdown(f"""<div class="output-box">
                <span class="label">📎 File attached:</span> `{file_upload.name}`</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="output-box">
            <span class="label">📓 Output Filename:</span> `{notebook_filename}`</div>""", unsafe_allow_html=True)

        # Get the subtasks and generator for streaming agent output
        subtasks, agent_stream = generate_agent_stream(file_path, user_input)

        subtasks_html = str(subtasks).replace('\n', '<br>')
        st.markdown(f"""<div class="output-box">
                <span class="label">📋 Subtasks:</span><br> {subtasks}
                </div>""", unsafe_allow_html=True)
        
    for step in agent_stream:
        # print("STEP:", step)  # Debugging line to check the step content

        with chat_container:
            if hasattr(step, 'tool_calls') and step.tool_calls:
                match = re.search(r"arguments='(.*?)'", str(step.tool_calls), re.DOTALL)
                if match:
                    arguments = match.group(1)  #.encode('utf-8').decode('unicode_escape')  # Decode escaped characters
                    tool_calls_html = arguments.replace('\\n', '<br>')
                else:
                    tool_calls_html = str(step.tool_calls).replace('\n', '<br>')

                st.markdown(f"""<div class="output-box">
                    <span class="label">🔧 Tool Call:</span><br> <code>{tool_calls_html}</code>
                    </div>""", unsafe_allow_html=True)
                
            if hasattr(step, 'model_output') and step.model_output:
                model_output_html = str(step.model_output).replace('\n', '<br>')
                st.markdown(f"""<div class="output-box">
                    <span class="label">💡 Model Output:</span><br>{model_output_html}
                    </div>""", unsafe_allow_html=True)
                
            if hasattr(step, 'observations') and step.observations:
                observations_html = str(step.observations).replace('\n', '<br>')
                st.markdown(f"""<div class="output-box">
                    <span class="label">🔍 Observations:</span><br>{observations_html}
                    </div>""", unsafe_allow_html=True)
                
            if hasattr(step, 'action_output') and step.action_output and str(step.action_output) != "None":
                action_output_html = str(step.action_output).replace('\n', '<br>')
                st.markdown(f"""<div class="output-box">
                    <span class="label">✅ Final Output:</span><br>{action_output_html}
                    </div>""", unsafe_allow_html=True)
    
    
    st.success("✅ Analysis complete!")

    notebook_path = os.path.join(os.getcwd(), notebook_filename)
    if os.path.exists(notebook_path):
        with open(notebook_path, "rb") as f:
            st.download_button(
                label="📥 Download Notebook",
                data=f,
                file_name=notebook_filename,
                mime="application/x-ipynb+json"
            )

                
                
                


