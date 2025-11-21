# AI recommendations service
import os
import httpx

GROQ_API_KEY = os.getenv("LLM_API_KEY_GROQ")
GROQ_API_URL = "https://api.groq.ai/v1/generate"  # Replace with actual Groq API endpoint

async def get_financial_advice(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    json_data = {
        "model": "groq-llm-free",  # Replace with actual model name
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=json_data)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "")
