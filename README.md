# 🤖 AI Agent Template Repository

## 📌 Overview

This repository provides a standardized template for building and deploying **developer AI agents** with automated sandbox provisioning, GitHub integration, and iterative development support.

It ensures isolated environments per request, automated repo setup, and seamless collaboration between developers and AI agents.

---

## 🎯 Objective

- Provide isolated sandbox shells per developer request  
- Automate GitHub repo creation and branch management  
- Enable AI agents to interpret tasks and generate code  
- Support iterative bug fixing via GitHub comments  
- Simplify deployment and CI/CD integration  

---

## 📂 Repository Structure

This template follows a standardized structure:

faas-template/
│
├── build.gradle        → Gradle tasks (build-agent, push-agent, deploy-agent)
├── function.yml        → Agent configuration (sandbox, GitHub, tools)
├── deps.gradle         → External dependencies
│
├── src/                → Source code (developer working directory)
│   ├── function/
│   │   ├── handler.py        → Core agent handler (init_sandbox, execute_task, chat_gpt_agent)
│   │   ├── requirements.txt  → Python dependencies (PyGithub, GPT agent bindings)
│   │   ├── handler_test.py   → Unit tests
│
├── app/                → Client application using this AI agent
│
└── README.md

Code

**Notes:**
- `src/function/handler.py` contains the agent logic  
- `src/function/requirements.txt` manages dependencies  
- `app/` contains client applications invoking the agent  

---

## 🛠️ Sandbox Behavior

- A **sandbox** is created per request ID  
- Tools listed in the template are installed automatically  
- GitHub repo/branch is provisioned via API  
- Sandbox metadata is mapped to the request ID for future calls  

**.gitignore requirement:**
build/
sandbox/

Code

---

## 🔄 Development Flow (CI – Test Server)

1. Developer submits requirement via agent function  
2. AI agent interprets task → generates code  
3. Code pushed to GitHub repo/branch  
4. Pull Request created → `main`  
5. Jenkins Test Server triggered  
6. Build and test execution  
7. Reviewer comments processed by agent  
8. Iteration until approval  

**CI Responsibilities:**
- Execute agent tasks  
- Run unit tests (`handler_test.py`)  
- Validate functionality before merge  

---

## 🚀 Production Flow (CD – Production Server)

1. Code merged to `main`  
2. Production Jenkins triggered  
3. Clean build execution  
4. Test verification  
5. Docker image creation  
6. Push image to registry  
7. Deployment executed per template instructions  

---

## 📦 Deployment Model

- Docker images published to a central registry  
- Client systems can:
  - Pull the image  
  - Import into container runtime  
  - Deploy using sandbox instructions  

---

## 🔁 Client Usage

Any client machine with:

- Docker  
- Python runtime  
- GitHub access token  

Can:

- Initialize sandbox → Submit tasks → Iterate with agent  

This supports:

- Remote execution  
- Multi‑developer usage  
- Automated bug fixing and deployment  

---

## 🧪 Testing Strategy

- **Test file location:** `src/function/handler_test.py`  

**Standard test function:**
```python
def test_handler():
    # Example test case
    assert True

---

**## Notes:**

A default test is included

Developers should extend test cases to cover new functionality

Tests run automatically during CI pipelines
