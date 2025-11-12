# LLM4ELN llm4eln-assessment - Basic LLM Capabilities with LangChain <!-- omit in toc -->

This tutorial will guide you through setting up a Python environment and working with Large Language Models (LLMs) using LangChain.

## Table of Contents <!-- omit in toc -->

- [1. Install uv (Fast Python Package Manager)](#1-install-uv-fast-python-package-manager)
- [2. Create Project and Virtual Environment](#2-create-project-and-virtual-environment)
- [3. Create a `.env` File](#3-create-a-env-file)
- [4. Initialize a LLM Object](#4-initialize-a-llm-object)
- [5. Use the model with a simple prompt](#5-use-the-model-with-a-simple-prompt)
- [6. Create a proof file](#6-create-a-proof-file)
- [7. Push your proof](#7-push-your-proof)

## 1. Install uv (Fast Python Package Manager)

Install uv on Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or on Windows with PowerShell

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> See [uv docs](https://docs.astral.sh/uv/getting-started/installation/) for more information

## 2. Create Project and Virtual Environment

1. First create your own fork: [https://github.com/LLM4ELN/llm4eln-assessment/fork](https://github.com/LLM4ELN/llm4eln-assessment/fork)

2. Then clone your fork and set up the project:

    ```bash
    git clone https://github.com/<YOUR_GITHUB_USERNAME>/llm4eln-assessment
    # or use ssh if you have configured ssh keys
    # git clone git@github.com:<YOUR_GITHUB_USERNAME>/llm4eln-assessment.git
    cd llm4eln-assessment
    ```

3. Ensure Python 3.12 is installed

    ```bash
    uv python install 3.12
    ```

4. Initialize Python project with uv

    ```bash
    uv init --python 3.12
    ```

5. Create local virutal environment

    ```bash
    uv venv
    ```

6. Activate Virtual Environment

    On Windows

    ```bash
    .venv\Scripts\activate
    ```

    Or on Linux

    ```bash
    source .venv/bin/activate
    ```

7. Install required packages

    ```bash
    uv add langchain langchain-openai langchain-ollama langchain-anthropic langchain-google-genai langchain-ollama python-dotenv
    ```

## 3. Create a `.env` File

See [`.env.example`](.env.example)

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

# Blablador
API_PROVIDER=blablador
API_ENDPOINT=https://api.helmholtz-blablador.fz-juelich.de/v1/
API_MODEL=alias-code
API_KEY=<your-api-key>
```

## 4. Initialize a LLM Object

See [`tutorial.py`](tutorial.py)

```py
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
# ToDo: Gemini, Anthropic etc.
```

## 5. Use the model with a simple prompt

```py
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

## 6. Create a proof file

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

## 7. Push your proof

```bash
git add proof/<your_proof_file>.txt
git commit -m "Add proof file for <user_name>"
git push origin main
```

Create a pull request by visiting

```txt
https://github.com/LLM4ELN/llm4eln-assessment/compare/main...<your_username>:llm4eln-assessment:main
```
