import asyncio
import logging
import openai
from abc import ABC, abstractmethod
from collections import deque

logger = logging.getLogger(__name__)

class LLMEngine(ABC):
    @abstractmethod
    def __init__(self, system_prompt):
        pass

    @abstractmethod
    async def _check_token_overload(self):
        pass

    @abstractmethod
    async def _manage_token_overload(self):
        pass

    @abstractmethod
    async def query(self, text: str) -> str:
        pass


class OpenAILLMEngine:
    AVAILABLE_MODELS = {
        'gpt-4': 4096,
        'gpt-3.5-turbo': 4096
        }
    MIN_QUEUE_LENGTH = 2

    def __init__(self, api_key: str, model: str = 'gpt-4', system_prompt: str = ''):
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model must be one of {self.AVAILABLE_MODELS}")
        openai.api_key = api_key
        self.model = model
        self.client = openai.AsyncOpenAI()
        self.system_prompt = system_prompt
        self.messages = deque([self._create_message(system_prompt, 'system')])
        self.token_limit = self._define_token_overload_threshold(model)

    def _create_message(self, text: str, role: str = 'user'):
        return {"role": role, "content": text}

    async def add_to_thread(self, text: str, role: str = 'user'):
        self.messages.append(self._create_message(text, role))
        if await self._check_token_overload():
            await self._manage_token_overload()

    async def clear_message_queue(self):
        self.messages.clear()
        if self.system_prompt:
            await self.add_to_thread(self.system_prompt, role='system')

    async def query(self, text: str, *args, clear_messages=False, **kwargs) -> str:
        await self.add_to_thread(text)
        await self._manage_token_overload()
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=list(self.messages),
            *args,
            **kwargs
        )
        response_content = response.choices[0].message.content.strip()
        self.messages.append(self._create_message(response_content, 'assistant'))
        await self._manage_token_overload()
        return response_content

    async def _check_token_overload(self):
        total_tokens = sum(len(m['content']) for m in self.messages)
        return total_tokens > self.token_limit

    def _define_token_overload_threshold(self, model):
        # This should ideally query the API or fetch from a dynamic source
        return self.AVAILABLE_MODELS.get(model, 4096)

    async def _manage_token_overload(self, range_warning: bool = False):
        while await self._check_token_overload():
            if (len(self.messages) <= self.MIN_QUEUE_LENGTH) and range_warning:
                logger.warn(f"Queue size is under {self.MIN_QUEUE_LENGTH}")
            self.messages.popleft()

# Usage example
async def main(api_key):
    engine = OpenAILLMEngine(api_key, model='gpt-4', system_prompt="Hello, I'm here to help.")
    response = await engine.query("How are you?")
    print(response)

if __name__ == "__main__":
    import config
    print(config.settings.to_dict())
    asyncio.run(main(config.settings["OPENAI_API_KEY"]))
