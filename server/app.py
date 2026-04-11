import uvicorn
from fastapi import FastAPI, Body
from server.env import CodeReviewerGym

app = FastAPI()
gym = CodeReviewerGym()

@app.get("/health")
async def health(): return {"status": "healthy"}

@app.post("/reset")
async def reset(data: dict = Body(default={})):
    return {"observation": gym.reset(data.get("task_id"))}

@app.post("/step")
async def step(action: dict = Body(...)):
    return gym.step(action)

def main(): uvicorn.run(app, host="0.0.0.0", port=7860)
if __name__ == "__main__": main()