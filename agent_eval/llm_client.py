import requests

def call_llm(
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
) -> str:

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": temperature,
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


