from huggingface_hub import InferenceClient
import os
from app.services.personality.prompt_builder import build_messages
from app.services.ai.memory import MemoryService

class ChatService:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_API_KEY"))
        self.memory = MemoryService()

    async def generate_response(self, channel_id, user_id, message):

        history = await self.memory.get_history(channel_id)

        messages = build_messages(message)

        if history:
            messages = [messages[0]] + history + [{"role": "user", "content": message}]

        result = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages,
            max_tokens=200,
            temperature=0.8
        )

        response = result.choices[0].message.content

        # salvar histórico
        await self.memory.add_message(channel_id, "user", message)
        await self.memory.add_message(channel_id, "assistant", response)

        return response