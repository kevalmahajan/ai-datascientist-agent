# 🧠 AutoPilot DS – Autonomous AI Agent for Jupyter Notebooks

**AutoPilot DS** is an intelligent AI agent designed to automate your entire data science workflow directly within a Jupyter Notebook. Just tell it what you want to accomplish in natural language — whether it's data analysis, model building, or running a full experiment — and it takes care of the rest.

For detailed explanation: [Check this out](https://www.youtube.com/watch?v=3t7bkWXEFhI)
---

## 🚀 Key Features

- **1. Task Understanding**  
  Accepts high-level instructions (e.g., "Build a classifier for this dataset") and translates them into executable data science workflows.

- **2. Data-Aware**  
  Reads and understands datasets in your environment to tailor its analysis and model-building approach.

- **3. Subtask Decomposition**  
  Breaks down complex tasks into manageable subtasks, executed sequentially.

- **4. Auto Analysis & Modeling**  
  Performs EDA, feature engineering, model selection, training, and evaluation — all autonomously.

- **5. Notebook Control**  
  Dynamically creates, edits, and executes code and markdown cells in the notebook to document and perform tasks.

- **6. Error Resilience**  
  Detects, analyzes, and recovers from errors during execution. Automatically retries failed subtasks with intelligent debugging.

---

## 🔧 Use Cases

- Rapid prototyping and experimentation  
- Teaching and learning data science through auto-documented notebooks  
- Automating repetitive analysis tasks  
- Enhancing productivity for data scientists and ML engineers

---

## 📦 Getting Started

> Just open your Jupyter Notebook, load the agent, and start with a prompt like:

```python
"Analyze the dataset and build a regression model to predict housing prices."
```
<br><br>
> ⚠️ **Note:** The output quality heavily depends on the LLM you are using.  
> 💡 **Tip:** For the best results, try using the **Gemini 2.5 Pro** model if available.



> [colab](https://colab.research.google.com/) has this similar feature integrated in gemini chat. I have tried to build something similar from scratch.
---

## 📁 Project Structure

- `tools/`: Contains tools to control python notebook utilized by the AI agent.
- `nb_agent_backend.py`: This file is the backend for our notebook AI agent.
- `nb_agent_ui.py`: This file is the streamlit UI for our notebook AI agent.
- `prompts/`: Contains the prompt templates for the AI agents.
- `tested_notebooks/`: Contains sample notebooks that I have tested, fully created and executed by the AI agent.

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone [https://github.com/your-username/ai-notebook-agent.git](https://github.com/kevalmahajan/ai-datascientist-agent)
cd ai-notebook-agent
````

### 2. Create virtual environment
```bash
.venv\Scripts\activate
source .venv/bin/activate
````


### 3. Install Dependencies

You can install the dependencies using **pip** *or* **uv**:

#### Option A: Using pip

```bash
pip install -r requirements.txt
```

#### Option B: Using uv

> [uv](https://github.com/astral-sh/uv) is a fast, modern Python package manager.

```bash
uv pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run nb_agent_ui.py
```

Make sure to replace `app.py` with the actual filename of your Streamlit entry point if different.

---

## 🧪 Tested Notebooks

Check the `tested_notebooks/` folder for example notebooks created entirely by the AI agent.

---

## 📌 Requirements

* Python 3.8+
* Jupyter
* Streamlit

All other dependencies are listed in `requirements.txt`.


## 💡 Tasks to Boost Your Knowledge
Some recommendations that you can try out to enhance this project
1. Try executing the code cells as sandbox environment
2. Try out this MCP server for jupyter notebook: [jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server)



