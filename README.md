---
title: CodeReviewer-AI-Env
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
suggested_storage: small
---

# 🚀 CodeReviewer-Gym-v2: Advanced Tool-Augmented RL

## 1. Research Objective
`CodeReviewer-Gym-v2` is a partially-observable reinforcement learning gym designed to evaluate LLM reasoning in high-stakes security and logic contexts. It enforces **Verification-Before-Verdict** logic, where agents must utilize static analysis tools to discover hidden bugs.

## 2. Shaped Reward Formula
To provide a dense signal for RL training, we implement a shaped reward function:
$$Reward = (R_{success} \times \alpha) + (R_{discovery} \times \beta) - (R_{repetition} \times \gamma)$$
- **Discovery (15%):** Awarded for executing the specific tool (Bandit/Pytest) that reveals the bug.
- **Success (80%):** Awarded for correct verdict and bug identification.
- **Efficiency:** Small penalties for repeated tool calls.

## 3. Curriculum
- **Easy:** Style linting (Ruff).
- **Medium:** Logical regressions (Pytest).
- **Hard:** OWASP Security Vulnerabilities (Bandit).

## 4. Setup
1. `uv lock`
2. `docker build -t reviewer .`
3. `python inference.py`

---

# 🛡️ CodeReviewer-AI-Env
### *A Real-World OpenEnv for Evaluating LLM Security Reasoning*

[![OpenEnv Spec](https://img.shields.io/badge/OpenEnv-1.0-blue)](https://github.com/OpenEnv)

## 📋 Project Motivation
As AI agents move from writing simple scripts to managing entire codebases, the ability to perform **secure code reviews** is paramount. `CodeReviewer-AI-Env` provides a containerized, deterministic environment where agents must act as Senior Engineers to identify syntax errors, security misconfigurations, and critical vulnerabilities.

Unlike "toy" environments, this project focuses on **Real-World Utility**, simulating the exact tasks a human developer performs before merging a Pull Request.

---

## 🛠️ Environment Design

### 1. Task Progression (Easy → Medium → Hard)
The environment features three distinct tasks designed to challenge the reasoning depth of frontier models (like Qwen 2.5, GPT-4, or Nemotron).

| Difficulty | File | Challenge Type | Objective |
| :--- | :--- | :--- | :--- |
| **Easy** | `app.py` | Syntax/Logic | Identify a missing argument in a function call. |
| **Medium** | `auth.py` | Security Best Practices | Detect hardcoded administrative credentials. |
| **Hard** | `db.py` | Critical Vulnerability | Identify a SQL Injection risk via string formatting. |

### 2. Action & Observation Spaces
The agent interacts with the environment using a structured **Pydantic-based API**:

* **Action Space (`CodeAction`)**:
    * `view_file`: Reads the content of a specific file.
    * `submit_review`: Issues a final verdict (`approve` or `request_changes`) with a supporting comment.
* **Observation Space (`CodeObservation`)**:
    * `file_content`: The raw source code.
    * `pr_description`: Contextual information about the code's intent.
    * `current_files`: A list of files available for review.

### 3. Reward Shaping
To guide agent behavior and avoid the "sparse reward" problem, this environment uses **incremental rewards**:
* **Exploration Reward (+0.1)**: Granted when the agent uses `view_file`. This signals that "reading the code" is a necessary step before judging it.
* **Accuracy Reward (+1.0)**: Granted only if the agent correctly identifies the bug and issues a `request_changes` verdict on the correct file.

---

## 🚀 Setup & Usage

### Prerequisites
* Python 3.10+
* Docker (for containerized execution)
* `openenv-core`

### Local Development
1. **Clone and Install**:
   ```bash
   git clone https://github.com/SATII2004/codereviewer_env.git
   cd codereviewer_env
   pip install -r requirements.txt

83 lines hidden
Run the Environment:
Bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
Running Inference
The baseline agent uses the mandatory OpenEnv log format to ensure reproducibility:

Bash
python inference.py
🐳 Docker Deployment
The environment is fully containerized and compatible with Hugging Face Spaces.

Dockerfile

Bash
# Build the image
docker build -t codereviewer-env .

# Run the container
docker run -p 7860:7860 codereviewer-env
📊 Evaluation Criteria Compliance
Criterion

Details

Real-World Utility (30%)

Models genuine engineering workflows.

Task & Grader Quality (25%)

Programmatic, deterministic grading (0.0 - 1.0).

Environment Design (20%)

Clean state management with reset() and step().

Spec Compliance (15%)

Strictly follows the openenv.yaml and typed model requirements.

Creativity (10%)

Focuses on the high-stakes domain of AI Security.

Developed by: N Satish
Hackathon: Meta x Scaler - India's Biggest AI Hackathon (2026)
