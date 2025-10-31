from dotenv import load_dotenv
from os import environ
load_dotenv()

# Initialize the language model

if environ.get("API_PROVIDER") == "azure":
    # https://docs.langchain.com/oss/python/integrations/providers/microsoft
    from langchain_openai import AzureChatOpenAI
    llm = AzureChatOpenAI(
        azure_deployment=environ.get("API_MODEL"),  # or your deployment
        api_version=environ.get("API_VERSION"),  # or your api version
        api_key=environ.get("API_KEY"),  # or your api key
        azure_endpoint=environ.get("API_ENDPOINT")
    )

if environ.get("API_PROVIDER") == "ollama":
    # https://docs.langchain.com/oss/python/integrations/chat/ollama
    from langchain_ollama import ChatOllama
    llm = ChatOllama(model=environ.get("API_MODEL"))

# ToDo: Gemini, Anthropic etc.

messages = [
    (
        "system",
        "You are a helpful assistant called 'LLM4ELN'."
        "Your purpose is to help users of electronic lab notebook."
    ),
    ("human", "What is your purpose?"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
