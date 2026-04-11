import random
from server.tasks import TASK_CORPUS
from server.tools import ToolEngine

class CodeReviewerGym:
    def __init__(self):
        self.engine = ToolEngine()
        self.reset()

    def reset(self, task_id=None):
        self.task_id = task_id or random.choice(list(TASK_CORPUS.keys()))
        self.task = TASK_CORPUS[self.task_id]
        self.steps = 0
        self.history = []
        self.discovery = False
        return {"observation": f"Task: {self.task_id}. Files: {list(self.task['files'].keys())}"}

    def step(self, action):
        self.steps += 1
        tool = action.get("tool")
        args = action.get("args") or {}
        
        if tool == "ls": res = self.engine.run_ls(self)
        elif tool == "read_file": res = self.engine.read_file(self, args.get("filename"))
        elif tool == "run_ruff": res = self.engine.run_ruff(self)
        elif tool == "run_bandit": 
            res = self.engine.run_bandit(self)
            if "Issue" in res["output"]: self.discovery = True
        elif tool == "run_pytest": 
            res = self.engine.run_pytest(self)
            if "FAILED" in res["output"]: self.discovery = True
        elif tool == "submit_review": return self._grade(action)
        else: res = {"error": "Invalid tool"}

        self.history.append(tool)
        reward = 0.05 if tool not in self.history[:-1] else -0.02
        return {"observation": str(res), "reward": reward, "done": self.steps >= 10, "info": {}}

    def _grade(self, action):
        correct = action.get("verdict") == "request_changes"
        score = 0.80 if correct else 0.05
        if self.discovery: score += 0.15
        return {"observation": "Done", "reward": min(0.99, score), "done": True, "info": {}}