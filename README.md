# Self-assessment - Basic LLM Capabilities with LangChain

This tutorial will guide you through setting up a Python environment and working with Large Language Models (LLMs) using LangChain.


### 1. Install uv (Fast Python Package Manager)

```bash
### Install uv

curl -LsSf https://astral.sh/uv/install.sh | sh

### Or on Windows with PowerShell

powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Project and Virtual Environment

```bash
### Create new project

git clone https://github.com/LLM4ELN/self-assessment
cd self-assessment

### Initialize Python project with uv

uv init
uv venv .venv --python 3.12
.venv\Scripts\activate

### Install required packages

uv add langchain langchain-openai langchain-ollama langchain-anthropic langchain-google-genai langchain-ollama python-dotenv
```

### 3. Create a .env file

see `.env.example`

```env
# use one (!) of the following configurations

# Azure OpenAI
API_PROVIDER=azure
API_KEY=<your-api-key>
API_ENDPOINT=https://your-deplyoment.openai.azure.com/ # example
API_VERSION=2024-10-21 # example
API_MODEL=gpt-5-nano-2025-08-07 # example

# ollama
API_PROVIDER=ollama
API_MODEL=deepseek-r1:7b # example
```

### 4. Initialize a LLM object

see `tutorial.py`

```python
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
```

### 5. Use the model with a simple prompt

```python
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
```

### 6. Create a proof file

```py
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
    f.write(environ.get('API_MODEL', '') + ":\n" + ai_msg.content)
```

### 7. Push your proof

Create a branch '<user_name>-proof'
```
git checkout -b <user_name>-proof
git add proof/<your_proof_file>.txt
git commit -m "Add proof file for <user_name>"
git push origin <user_name>-proof
```