from .mori import MORI_PROFILE

def build_messages(user_message: str, memory: str | None = None, mood: str = "sereno"):
    memory_text = memory if memory else "Sem memórias relevantes."

    system_prompt = f"""{MORI_PROFILE}

Estado atual:
- Humor: {mood}

Memória relevante:
{memory_text}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]