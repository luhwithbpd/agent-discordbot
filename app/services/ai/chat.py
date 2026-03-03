from huggingface_hub import InferenceClient
import os
import asyncio
from app.services.personality.prompt_builder import build_messages
from app.services.ai.memory import MemoryService

class ChatService:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_API_KEY"))
        self.memory = MemoryService()

    async def generate_response(self, channel_id, user_id, message):
        history = await self.memory.get_history(channel_id)

        base = build_messages(message)  # mantém seu builder
        if history:
            messages = [base[0]] + history + [{"role": "user", "content": message}]
        else:
            messages = base

        def _call_hf():
            return self.client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=messages,
                max_tokens=200,
                temperature=0.8
            )

        try:
            result = await asyncio.wait_for(asyncio.to_thread(_call_hf), timeout=35)
            response = (result.choices[0].message.content or "").strip()
        except asyncio.TimeoutError:
            response = "Hm... a floresta ficou lenta. Tente de novo em um momento..."
        except Exception as e:
            print(f"[ChatService] Error: {repr(e)}")
            response = "Hm... algo interrompeu o vento por aqui."

        await self.memory.add_message(channel_id, "user", message)
        await self.memory.add_message(channel_id, "assistant", response)
        return response