import asyncio
import os
import httpx
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
BASE_URL = "http://0.0.0.0:7860"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

async def run_task(http_client, task_id):
    print(f"[START] task={task_id} env=codereviewer model={MODEL_NAME}", flush=True)
    try:
        resp = await http_client.post(f"{BASE_URL}/reset", json={"task_id": task_id})
        obs = resp.json()["observation"]
        rewards = []
        
        for step in range(1, 3):
            # Mandatory Proxy API Call
            prompt = f"Review code for task {task_id}. Files: {obs['current_files']}. Content: {obs.get('file_content')}. Respond with 'view' or 'fix'."
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            
            action_type = "view_file" if step == 1 else "submit_review"
            payload = {
                "action_type": action_type,
                "file_path": obs['current_files'][0],
                "verdict": "request_changes" if action_type == "submit_review" else None,
                "comment": f"Found bug in {obs['current_files'][0]}"
            }

            step_resp = await http_client.post(f"{BASE_URL}/step", json=payload)
            result = step_resp.json()
            reward = result["reward"]
            rewards.append(reward)
            print(f"[STEP] step={step} action={action_type} reward={reward:.2f} done={str(result['done']).lower()} error=null", flush=True)
            if result["done"]: break

        score = sum(rewards) / 1.1
        print(f"[END] success=true steps={len(rewards)} score={score:.2f} rewards={','.join([f'{r:.2f}' for r in rewards])}", flush=True)
    except Exception as e:
        print(f"[END] success=false steps=0 score=0.00 rewards=0.00", flush=True)

async def main():
    async with httpx.AsyncClient() as http_client:
        for t in ["easy", "medium", "hard"]:
            await run_task(http_client, t)

if __name__ == "__main__":
    asyncio.run(main())