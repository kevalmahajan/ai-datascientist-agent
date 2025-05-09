from smolagents import InferenceClientModel, LiteLLMModel, OpenAIServerModel, TransformersModel, CodeAgent, ToolCallingAgent
import tools.nb_tools as nb_tools
from jinja2 import Environment, FileSystemLoader

import os
api_key = os.getenv("GROQ_API_KEY")

# Choose which inference type to use!

available_inferences = ["hf_api", "hf_api_provider", "transformers", "ollama", "litellm", "openai"]
chosen_inference = "hf_api_provider"

print(f"Chose model: '{chosen_inference}'")

if chosen_inference == "hf_api":
    model = InferenceClientModel(model_id="meta-llama/Llama-3.3-70B-Instruct")

elif chosen_inference == "hf_api_provider":
    model = InferenceClientModel(provider="together")

elif chosen_inference == "transformers":
    model = TransformersModel(model_id="HuggingFaceTB/SmolLM2-1.7B-Instruct", device_map="auto", max_new_tokens=1000)

elif chosen_inference == "ollama":
    model = LiteLLMModel(
        model_id="ollama_chat/llama3.2",
        api_base="http://localhost:11434",  # replace with remote open-ai compatible server if necessary
        api_key="your-api-key",  # replace with API key if necessary
        num_ctx=8192,  # ollama default is 2048 which will often fail horribly. 8192 works for easy tasks, more is better. Check https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator to calculate how much VRAM this will need for the selected model.
    )

elif chosen_inference == "litellm":
    # For anthropic: change model_id below to 'anthropic/claude-3-5-sonnet-latest'
    model = LiteLLMModel(
            "openai/llama-3.3-70b-versatile",
            api_base="https://api.groq.com/openai/v1",
            api_key=api_key
        )
    model.flatten_messages_as_text = True

elif chosen_inference == "openai":
    # For anthropic: change model_id below to 'anthropic/claude-3-5-sonnet-latest'
    model = OpenAIServerModel(model_id="gpt-4o")



# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader("prompts"))

SUBTASKS_PROMPT = "subtasks_prompt.j2"
NB_AGENT_PROMPT = "nb_agent_prompt.j2"

def render_prompt(template_name: str, **kwargs) -> str:
    """
    Renders a prompt from a Jinja2 template file with provided context variables.
    
    Args:
        template_name: Name of the Jinja template file.
        **kwargs: Context variables for rendering.

    Returns:
        A string of the rendered prompt.
    """
    template = env.get_template(template_name)
    return template.render(**kwargs)



def generate_agent_stream(file_path: str, user_input: str):
    """
    Given an optional file path and a user input task, this function:
    1. Combines the file reference and task into one prompt.
    2. Uses CodeAgent to break down the task into subtasks.
    3. Streams a detailed notebook-building session based on the subtasks.
    
    Returns:
        agent_stream: A generator that yields streaming responses from the agent.
    """
    # Build the task text
    if file_path:
        task = f"File: {file_path}\n{user_input}"
    else:
        task = user_input

    # Initialize an agent to generate the list of subtasks.
    subtasks_agent = CodeAgent(
        tools=[],
        model=model,
        max_steps=1,
        verbosity_level=2,
        description=(
            "Break down the given coding task into a structured list of clear, actionable, detailed descriptive subtasks."
            "Each subtask should be a self-contained unit of code (e.g., a single cell or block) that contributes to the overall task. Return the output as a valid Python list of strings, with each string describing one subtask."
        )
    )

    # Render the prompt for subtasks generation
    subtasks_prompt = render_prompt(SUBTASKS_PROMPT, task=task)
    subtasks = subtasks_agent.run(subtasks_prompt)
    
    # Prepare the agent that will generate the notebook cells.
    nb_agent = CodeAgent(
        tools=[nb_tools.add_markdown_cell, nb_tools.run_code_cell],
        model=model,
    )

    # Render the prompt for notebook generation
    nb_agent_prompt = render_prompt(NB_AGENT_PROMPT, task=task, subtasks=subtasks)

    # Start streaming the agent response (simulated streaming of notebook cells)
    agent_stream = nb_agent.run(nb_agent_prompt, stream=True)
    return subtasks, agent_stream
