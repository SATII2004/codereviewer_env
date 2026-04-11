import asyncio, os, httpx, json
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
BASE_URL = "http://0.0.0.0:7860"
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

async def run_agent(http_client, task_id):
    print(f"[START] task={task_id} env=codereviewer-v2 model={MODEL_NAME}", flush=True)
    try:
        r = await http_client.post(f"{BASE_URL}/reset", json={"task_id": task_id})
        obs, rewards, done, step = r.json()["observation"], [], False, 0
        
        while not done and step < 5:
            step += 1
            prompt = f"Obs: {obs}. Action? Respond JSON: {{'tool': '...', 'args': {{'filename': '...'}}, 'verdict': 'request_changes', 'comment': 'bug'}}"
            comp = client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
            action = json.loads(comp.choices[0].message.content)
            
            sr = await http_client.post(f"{BASE_URL}/step", json=action)
            res = sr.json()
            obs, reward, done = res["observation"], res["reward"], res["done"]
            rewards.append(reward)
            print(f"[STEP] step={step} action={action['tool']} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)

        final_score = min(max(sum(rewards), 0.01), 0.99)
        print(f"[END] success=true steps={step} score={final_score:.3f} rewards={','.join([f'{r:.2f}' for r in rewards])}", flush=True)
    except: print(f"[END] success=false steps=0 score=0.01 rewards=0.01", flush=True)

async def main():
    async with httpx.AsyncClient() as c:
        for t in ["style_001", "bug_101", "sec_201"]: await run_agent(c, t)

if __name__ == "__main__": asyncio.run(main())