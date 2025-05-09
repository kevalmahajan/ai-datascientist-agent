import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from nbclient import NotebookClient
import os

from smolagents import tool


def create_noteboook(filename: str):
    global NOTEBOOK_PATH, notebook
    NOTEBOOK_PATH = filename

    # Load or initialize notebook
    if os.path.exists(NOTEBOOK_PATH):
        with open(NOTEBOOK_PATH) as f:
            notebook = nbformat.read(f, as_version=4)
    else:
        notebook = new_notebook()


def save_notebook():
    with open(NOTEBOOK_PATH, "w") as f:
        nbformat.write(notebook, f)

@tool
def run_code_cell(code: str) -> str:
    """Appends a code cell to the notebook, runs it, and returns the output of the last executed cell.

    Args:
        code: The Python code to execute in the code cell.

    Returns:
        str: The output of the last executed code cell.
    """
    code_cell = new_code_cell(code)
    notebook.cells.append(code_cell)
    save_notebook()

    client = NotebookClient(notebook, 
                            timeout=60, 
                            kernel_name="python3",
                            allow_errors=True)
    client.execute()
    save_notebook()

    last_cell = notebook.cells[-1]
    outputs = last_cell.get("outputs", [])

    if not outputs:
        return ""

    output = outputs[-1]  # Get only the last output
    if output.output_type == "stream":
        return output.text.strip()
    elif output.output_type == "execute_result":
        return output.get("data", {}).get("text/plain", "").strip()
    elif output.output_type == "error":
        return f"{output.ename}: {output.evalue}".strip()

    return ""


@tool
def add_markdown_cell(markdown: str) -> bool:
    """Appends a markdown cell to the notebook and saves it.

    Args:
        markdown: The markdown content to include in the cell.
    
    Returns:
        bool: Status of success or failure
    """
    md_cell = new_markdown_cell(markdown)
    notebook.cells.append(md_cell)
    save_notebook()
    return True


if __name__ == "__main__":

    # Create a new notebook
    create_noteboook("pandas_example_notebook.ipynb")

    # Markdown: Intro
    add_markdown_cell("# Pandas Data Analysis\nIn this notebook, we create a DataFrame and perform basic analysis.")

    # Code Cell 1: Create a DataFrame
    code1 = """
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

df = pd.DataFrame(data)
print(df)
"""
    out1 = run_code_cell(code1)
    print("Created DataFrame:\n", out1)

    # Markdown: Next step
    add_markdown_cell("## Filtering and Statistics\nWe'll now calculate the average age and filter by age > 30.")

    # Code Cell 2: Filter and analyze
    code2 = """
average_age = df['Age'].mean()
older_people = df[df['Age'] > 30]

print(f"Average Age: {average_age}")
print("\\nPeople older than 30:")
print(older_people)
"""
    out2 = run_code_cell(code2)
    print("Analysis output:\n", out2)

    # Markdown: Conclusion
    add_markdown_cell("### Summary\n- The average age is calculated.\n- People older than 30 are listed.")


