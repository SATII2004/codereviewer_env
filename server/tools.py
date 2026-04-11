class ToolEngine:
    @staticmethod
    def run_ls(env):
        return {"output": "\n".join(env.task["files"].keys())}

    @staticmethod
    def read_file(env, filename):
        content = env.task["files"].get(filename)
        return {"output": f"CODE:\n{content}"} if content else {"error": "File not found"}

    @staticmethod
    def run_ruff(env):
        return {"output": env.task["tool_outputs"].get("run_ruff", "Clean")}

    @staticmethod
    def run_bandit(env):
        return {"output": env.task["tool_outputs"].get("run_bandit", "Clean")}

    @staticmethod
    def run_pytest(env):
        return {"output": env.task["tool_outputs"].get("run_pytest", "Passed")}