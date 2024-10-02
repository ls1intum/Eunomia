from app.common.environment import config
from app.models.base_model import BaseModelClient
from app.models.ollama_model import OllamaModel
from app.models.openai_azure_model import AzureOpenAIModel
from app.models.openai_model import OpenAIModel

default_model_name = "llama3.1:70b"


def get_model_client() -> BaseModelClient:
    use_openai = config.USE_OPENAI.lower() == "true"
    if use_openai:
        if not config.USE_AZURE == "true":
            return OpenAIModel(model=config.OPENAI_MODEL, api_key=config.OPENAI_API_KEY)
        else:
            return AzureOpenAIModel(model=config.OPENAI_MODEL, azure_deployment=config.AZURE_DEPLOYMENT)
    else:
        return OllamaModel(model=config.GPU_MODEL, embed_model=config.EMBED_MODEL, url=config.OLLAMA_URL)
