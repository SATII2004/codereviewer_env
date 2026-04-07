import asyncio
from models import CodeAction, CodeObservation
import os

class CodeReviewEnv:
    def __init__(self):
        self.tasks = {
            "easy": {"file": "app.py", "content": "def add(a, b):\n    return a + b\nprint(add(5)) # Missing second argument!", "bug_line": 3},
            "medium": {"file": "auth.py", "content": "def check_pass(p):\n    if p == 'admin123': return True\n    else: return False", "bug_line": 2}, # Hardcoded creds
            "hard": {"file": "db.py", "content": "query = f'SELECT * FROM users WHERE id = {user_id}'\nexecute(query)", "bug_line": 1} # SQL Injection
        }
        self.current_task_id = os.getenv("TASK_ID", "easy")
        self.step_count = 0

    async def reset(self):
        self.step_count = 0
        task = self.tasks[self.current_task_id]
        return CodeObservation(
            pr_description=f"Review the code in {task['file']} for bugs.",
            current_files=[task['file']]
        )

    async def step(self, action: CodeAction):
        self.step_count += 1
        task = self.tasks[self.current_task_id]
        reward = 0.0
        done = False
        obs = CodeObservation(pr_description="Reviewing...", current_files=[task['file']])

        if action.action_type == "view_file":
            obs.file_content = task['content']
            reward = 0.1 
        
        elif action.action_type == "submit_review":
            done = True
            if action.verdict == "request_changes" and task['file'] in (action.comment or ""):
                reward = 1.0
            else:
                reward = 0.0
        
        if self.step_count >= 5: done = True
        return obs, reward, done, {}