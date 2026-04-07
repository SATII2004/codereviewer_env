import asyncio
import os
import httpx
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY") or "sk-dummy"

BASE_URL = "http://0.0.0.0:7860"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

async def run_inference():
    async with httpx.AsyncClient() as http_client:
        print(f"[START] task=easy env=codereviewer model={MODEL_NAME}", flush=True)
        
        try:
            resp = await http_client.post(f"{BASE_URL}/reset")
            resp_data = resp.json()
            obs = resp_data["observation"]
            
            rewards = []
            steps_taken = 0
            
            for step in range(1, 3):
                steps_taken = step
                action_type = "view_file" if step == 1 else "submit_review"
                
                action_data = {
                    "action_type": action_type,
                    "file_path": "app.py",
                    "verdict": "request_changes" if action_type == "submit_review" else None,
                    "comment": "Found bug in app.py" if action_type == "submit_review" else None
                }

                step_resp = await http_client.post(f"{BASE_URL}/step", json=action_data)
                result = step_resp.json()
                
                reward = result["reward"]
                done = result["done"]
                rewards.append(reward)
                
                print(f"[STEP] step={step} action={action_type} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)
                
                if done: 
                    break

            total_reward = sum(rewards)
            final_score = min(max(total_reward / 1.1, 0.0), 1.0)
            success = "true" if final_score >= 0.5 else "false"
            
            rewards_str = ",".join([f"{r:.2f}" for r in rewards])
            print(f"[END] success={success} steps={steps_taken} score={final_score:.2f} rewards={rewards_str}", flush=True)

        except Exception as e:
            print(f"Error during inference: {e}")
            print(f"[END] success=false steps=0 score=0.00 rewards=0.00", flush=True)

if __name__ == "__main__":
    asyncio.run(run_inference())