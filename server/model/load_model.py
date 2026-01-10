from smolagents import HfApiModel,LiteLLMModel
import os

model_id="ollama_chat/tinyllama:latest"

def load_model():
    model = LiteLLMModel(model_id=model_id,api_key="ollama")
    return model
