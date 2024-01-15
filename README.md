# Semantic Kernel Integration with OpenAI and Bing Search

This project demonstrates the integration of the Semantic Kernel with OpenAI's GPT-3.5-turbo and Bing Search API. It includes custom skills for joke generation and web searching, along with action and stepwise planning functionalities.

## Features

- Integration with OpenAI's GPT-3.5-turbo for chat services.
- Bing Search API integration for web searching.
- Custom skills for generating jokes and performing web searches.
- Action and Stepwise planning for executing tasks based on user prompts.

## Installation

Before running the project, ensure you have Python and Poetry installed on your system. Then, install the required dependencies:

```bash
poetry install 
poetry run python main.py
```

## Env File
Make sure you create a .env file in the project root directly with following values

```commandline
OPENAI_API_KEY=your_openai_api_key
ORG_ID=your_organization_id
BING_API_KEY=your_bing_api_key
```
