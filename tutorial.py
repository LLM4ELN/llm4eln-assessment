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

if environ.get("API_PROVIDER") == "blablador":
    # https://sdlaml.pages.jsc.fz-juelich.de/ai/guides/blablador_api_access/
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model=environ.get("API_MODEL"),
        api_key=environ.get("API_KEY"),
        base_url=environ.get("API_ENDPOINT")
    )

if environ.get("API_PROVIDER") == "openai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(api_key=environ.get("API_KEY"))

if environ.get("API_PROVIDER") == "chatai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        api_key=environ.get("API_KEY"),
        openai_api_base=environ.get("API_ENDPOINT"),
        model=environ.get("API_MODEL")
    )

if environ.get("API_PROVIDER") == "gemini":
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402
    llm = ChatGoogleGenerativeAI(
        api_key=environ.get("API_KEY"),
        model=environ.get("API_MODEL")
    )

messages = [
    (
        "system",
        "You are a helpful assistant called 'LLM4ELN'."
        "Your purpose is to help users of electronic lab notebook."
    ),
    ("human", "What is your purpose?"),
]
ai_reply = llm.invoke(messages)
if isinstance(ai_reply, str):
    ai_msg = ai_reply
else:
    ai_msg = ai_reply.content
print("AI:", ai_msg)

# store a proof file

import subprocess  # noqa: E402

username = subprocess.run(
    ["git", "config", "user.name"],
    capture_output=True,
    text=True,
    check=True
).stdout.strip()

import hashlib  # noqa: E402

hash_value = hashlib.sha256(
    (username + str(messages)).encode()
).hexdigest()

file_name = f"{username}_{environ.get('API_PROVIDER')}_proof_{hash_value}.txt"
with open(f"./proof/{file_name}", "w") as f:
    f.write(environ.get('API_MODEL', '') + ":\n" + ai_msg)
