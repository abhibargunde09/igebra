
***AI Agent for Personalized Learning***

LermoAI is an open-source project for personalized learning, offering chat, search, article writing, podcast creation, and video generation tailored to your learning style.



# Features

- [x] AI Agent
- [x] Article Generation
- [x] Podcast Generation
- [x] LLM
  - [x] OpenAI
  - [x] Mistral
  - [x] Llama
  - [ ] Groq
  - [ ] Claude
- [ ] Learning Path
- [ ] Chat Agent
- [ ] Video Generation
- [ ] Custom Agent
- [ ] Search Agent

# Getting Started

### Requirements

- Node.js
- Next.js
- React
- Python

### Web

To set up the frontend:

```sh
cd apps/frontend/apps/lermo-gen-web

# Install Dependencies
pnpm i

# Start
pnpm run dev
```

### API

To set up the API:

```sh
cd apps/api/core-api

# Install Dependencies
pip install -r requirements.txt
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download

# Start
python main.py
```

### LLM

LermoAI supports both OpenAI and self-hosted LLMs such as Llama and Mistral. For more details, refer to the [LLM README](apps/llm/README.md).

### Docker Setup

Edit the environment variables to use either OpenAI or your self-hosted LLM:

```yaml
# OpenAI
args:
  - OPENAI_API_BASE=https://api.openai.com/v1
  - OPENAI_API_KEY=sk-proj-xxx

# Hugging Face
args:
  - OPENAI_API_BASE=https://llama-cpp.hf.space
  - OPENAI_API_KEY=llama-key
```

To start the Docker containers:

```sh
docker-compose up
```
