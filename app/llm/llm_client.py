from app.config.settings import config
from tenacity import retry, stop_after_attempt, wait_random_exponential
from loguru import logger

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

@retry(wait=wait_random_exponential(min=1, max=2), stop=stop_after_attempt(2))
def call_robust_llm(system_prompt: str, user_prompt: str, json_mode: bool = False):
    try:
        llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            api_key=config.OPENAI_API_KEY,
            temperature=0,
        )

        if json_mode:
            llm = llm.bind(response_format={"type": "json_object"})

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        resp = llm.invoke(messages)   # <- FIX
        return resp.content
    except Exception as e:
        logger.info(f"Error calling llm {e}")
        raise





# if __name__ == "__main__":
#     print(call_robust_llm(
#         system_prompt="You are a helpful assistant",
#         user_prompt="What is 2+2?",
#         json_mode=False
#     ))

#     print(call_robust_llm(
#         system_prompt="You are a helpful assistant",
#         user_prompt="Return JSON with key answer for 2+2",
#         json_mode=True
#     ))
