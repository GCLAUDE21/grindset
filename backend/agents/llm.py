from backend.config import LLM_PROVIDER, LLM_MODEL

def get_llm():
    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=LLM_MODEL, temperature=0)
    elif LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=LLM_MODEL, temperature=0)
    else:
        raise ValueError(f"LLM provider inconnu : {LLM_PROVIDER}")