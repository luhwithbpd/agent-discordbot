from huggingface_hub import InferenceClient
import os

class ChatService:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_API_KEY"))

    async def generate_response(self, user_id, message):
        result = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {"role":"system","content":"Você é um assistente útil."},
                {"role":"user","content": message}
            ],
            max_tokens=200
        )
        return result.choices[0].message.content
        
        # except Exception as e:
        #     print(f"Error generating response: {e}")
        #     return "Desculpe, ocorreu um erro ao processar sua mensagem."