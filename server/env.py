class CodeReviewEnv:
    def __init__(self):
        self.tasks = {
            "easy": {
                "file": "app.py", 
                "content": "def add(a, b):\n    return a + b\nprint(add(5))", 
                "bug": "missing argument"
            },
            "medium": {
                "file": "auth.py", 
                "content": "def login(u, p):\n    if p == 'admin123': return True", 
                "bug": "hardcoded password"
            },
            "hard": {
                "file": "db.py", 
                "content": "query = f'SELECT * FROM users WHERE id = {user_id}'", 
                "bug": "sql injection"
            }
        }
        self.current_task_id = "easy"
        self.step_count = 0

    async def reset(self, task_id: str = "easy"):
        self.current_task_id = task_id
        self.step_count = 0
        task = self.tasks[self.current_task_id]
        return {
            "pr_description": f"Review {task['file']} for {task['bug']}.",
            "current_files": [task['file']]
        }

    async def step(self, action):
        self.step_count += 1
        task = self.tasks[self.current_task_id]
        reward = 0.0
        done = False
        
        if action.action_type == "view_file":
            reward = 0.1
            observation = {"file_content": task['content'], "pr_description": "Reviewing...", "current_files": [task['file']]}
        elif action.action_type == "submit_review":
            done = True
            # Grader: Did agent identify the bug in the right file?
            if action.verdict == "request_changes" and task['file'] in (action.comment or ""):
                reward = 1.0
            observation = {"pr_description": "Review Submitted", "current_files": [task['file']]}
        
        if self.step_count >= 5: done = True
        return observation, reward, done, {}