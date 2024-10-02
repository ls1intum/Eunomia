from openai.lib.azure import AzureOpenAI

from app.models.openai_model import OpenAIModel


class AzureOpenAIModel(OpenAIModel):
    azure_deployment: str

    def model_post_init(self, **kwargs):
        self._client = AzureOpenAI(
            azure_deployment=self.azure_deployment,
        )
        self.init_model()
