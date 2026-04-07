import uvicorn
from fastapi import FastAPI, Body
from server.env import CodeReviewEnv
from models import CodeAction

app = FastAPI()
env_instance = CodeReviewEnv()

@app.post("/reset")
async def reset(data: dict = Body(default={})):
    task_id = data.get("task_id", "easy")
    obs = await env_instance.reset(task_id=task_id)
    return {"observation": obs}

@app.post("/step")
async def step(action: CodeAction):
    obs, reward, done, info = await env_instance.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
async def state():
    return {"status": "running", "step": env_instance.step_count}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()