from collections import defaultdict

class MemoryService:
    def __init__(self):
        self.channel_conversations = defaultdict(list)

    async def add_message(self, channel_id, role, content):
        self.channel_conversations[channel_id].append({
            "role": role,
            "content": content
        })

        # limitar histórico
        self.channel_conversations[channel_id] = \
            self.channel_conversations[channel_id][-15:]

    async def get_history(self, channel_id):
        return self.channel_conversations[channel_id]