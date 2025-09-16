from dotenv import load_dotenv
from langchain.globals import set_debug, set_verbose
from langchain.tools.render import render_text_description
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import architect_prompt, coder_system_prompt, planner_prompt
from agent.states import CoderState, Plan, TaskPlan
from agent.tools import get_current_directory, list_files, read_file, write_file

_ = load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    
    # Define the tools available to the coder agent
    coder_tools = [read_file, write_file, list_files, get_current_directory]

    # Render the tool descriptions into a string that the LLM can understand.
    # This is the crucial step that solves the problem.
    tool_description_string = render_text_description(coder_tools)

    # Update the system prompt to include the precise tool descriptions.
    system_prompt = coder_system_prompt(tools=tool_description_string)

    # Read existing file content *after* defining tools, to keep logic clean.
    existing_content = read_file.run(current_task.filepath)

    user_prompt = (
        f"Here is the task you must perform:\n"
        f"Task: {current_task.task_description}\n"
        f"File to modify: {current_task.filepath}\n\n"
        f"Here is the current content of that file:\n"
        f"---BEGIN CURRENT CONTENT---\n{existing_content}\n---END CURRENT CONTENT---\n\n"
        "Use the provided tools to accomplish the task by writing the complete, final content to the file."
    )

    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


# Define the graph structure
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: END if s.get("status") == "DONE" else "coder",
)

graph.set_entry_point("planner")
agent = graph.compile()


if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)
