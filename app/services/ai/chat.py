from openai import AsyncOpenAI
import os

class ChatService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
            )
        pass

    async def generate_response(self, user_id: int, message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
            )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."