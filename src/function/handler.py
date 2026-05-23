import json
import uuid
from github import Github
from typing import Dict, Any
from gpt4all import GPT4All

# In-memory mapping of request_id -> sandbox/session
SANDBOX_MAP: Dict[str, Dict[str, Any]] = {}

def handler(request_id=None, template=None, task=None):
    """
    Args:
      request_id: str (optional) - existing sandbox ID
      template: str/dict (required for init) - XML/JSON template
      task: str (optional) - developer requirement/task

    Returns:
      dict with status/result
    """

    if request_id is None:
        # First init
        request_id = str(uuid.uuid4())
        if isinstance(template, str):
            template = json.loads(template)  # or parse XML
        sandbox = init_sandbox(template)
        SANDBOX_MAP[request_id] = sandbox
        return {"request_id": request_id, "status": "initialized"}

    else:
        # Subsequent call
        sandbox = SANDBOX_MAP.get(request_id)
        if not sandbox:
            return {"error": "Invalid request_id"}
        result = execute_task(sandbox, task)
        return {"request_id": request_id, "result": result}


def init_sandbox(template: Dict[str, Any]) -> Dict[str, Any]:
    # Create isolated environment (Docker/VM)
    # Install tools listed in template
    g = Github(template["github_token"])
    org = g.get_organization(template["github_org"])
    repo = org.create_repo(template["repo_name"])
    return {
        "repo": repo.full_name,
        "tools": template.get("tools", []),
        "instructions": template.get("instructions", "")
    }


def execute_task(sandbox: Dict[str, Any], task: str) -> str:
    # Call GPT agent to generate code/steps
    agent_response = chat_gpt_agent(task, sandbox)
    # Push code, open PR, respond to comments
    return f"Agent executed task: {task} in {sandbox['repo']} → {agent_response}"


def chat_gpt_agent(task: str, sandbox: Dict[str, Any]) -> str:
    model = GPT4All("mistral-7b-instruct")
    with model.chat_session() as session:
        response = session.prompt(f"Task: {task}\nTools: {sandbox['tools']}")
    return response

