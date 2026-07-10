# LLM Provider Setup

## Goals
- Free-first providers with graceful cascading fallback.
- Primary local model: Gemma 4-like local model via Ollama later when approved.
- JSON/schema-mode preferred for enrichment.

## Provider registration
Register providers under `apps/api/src/bookverse/llm/providers/`.

## Fallback chain
Primary: Gemini Free -> OpenRouter -> Mistral -> Groq -> SambaNova -> GitHub Models -> NVIDIA/Cerebras -> Local Ollama Gemma 4.
Each provider must fail once before the chain advances.

## Provider Quick Links
- Google AI Studio Gemini: https://aistudio.google.com/app/apikey
- OpenRouter: https://openrouter.ai/keys
- NVIDIA: https://build.nvidia.com
- Mistral: https://console.mistral.ai/
- SambaNova: https://sambanova.ai/
- Groq: https://console.groq.com/keys
- Cerebras: https://cerebras.ai/
- GitHub Models: https://github.com/marketplace/models
- Local Ollama Gemma 4: run locally after installation approval

## Env
Store keys in `.env` per `infra/compose/.env.example`.
