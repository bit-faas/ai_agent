import json
import uuid
from github import Github
from typing import Dict, Any
from gpt4all import GPT4All

# In-memory mapping of request_id -> sandbox/session
SANDBOX_MAP: Dict[str, Dict[str, Any]] = {}

def handle(*args, **kwargs):
    """
    OpenFaaS entry point.

    Supports:
    1. String body
       handle('{"request_id":"123","task":"hello"}')

    2. JSON object body
       handle(request_id="123", task="hello")
    """

    # Case 1: String request body
    if len(args) == 1 and isinstance(args[0], str):

        try:
            req = json.loads(args[0])
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON request"
            }

        return handler(
            request_id=req.get("request_id"),
            template=req.get("template"),
            task=req.get("task")
        )

    # Case 2: JSON body already converted to dict by index.py
    if kwargs:

        return handler(
            request_id=kwargs.get("request_id"),
            template=kwargs.get("template"),
            task=kwargs.get("task")
        )

    return {
        "error": "Invalid request format"
    }


def handler(request_id=None, template=None, task=None):
    """
    Args:
      request_id: str (optional) - existing sandbox ID
      template: str/dict (required for init) - JSON template
      task: str (optional) - developer requirement/task

    Returns:
      dict with status/result
    """

    if request_id is None:

        request_id = str(uuid.uuid4())

        if template is None:
            return {
                "error": "template is required for initialization"
            }

        if isinstance(template, str):
            template = json.loads(template)

        sandbox = init_sandbox(template)

        SANDBOX_MAP[request_id] = sandbox

        return {
            "request_id": request_id,
            "status": "initialized"
        }

    sandbox = SANDBOX_MAP.get(request_id)

    if not sandbox:
        return {
            "error": "Invalid request_id"
        }

    result = execute_task(sandbox, task)

    return {
        "request_id": request_id,
        "result": result
    }


def init_sandbox(template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create isolated environment and initialize repository.
    """

    g = Github(template["github_token"])

    org = g.get_organization(template["github_org"])

    repo = org.create_repo(template["repo_name"])

    return {
        "repo": repo.full_name,
        "tools": template.get("tools", []),
        "instructions": template.get("instructions", "")
    }


def execute_task(sandbox: Dict[str, Any], task: str) -> str:
    """
    Execute developer task through GPT agent.
    """

    agent_response = chat_gpt_agent(task, sandbox)

    return (
        f"Agent executed task: "
        f"{task} in {sandbox['repo']} "
        f"→ {agent_response}"
    )


def chat_gpt_agent(task: str, sandbox: Dict[str, Any]) -> str:
    """
    Run GPT4All agent.
    """

    model = GPT4All("mistral-7b-instruct")

    with model.chat_session() as session:
        response = session.prompt(
            f"Task: {task}\nTools: {sandbox['tools']}"
        )

    return response