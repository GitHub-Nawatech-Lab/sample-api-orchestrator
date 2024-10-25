from langchain_core.messages import BaseMessage
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

from app.dependencies import *
from app.func_call import func
from app.settings import settings


class OpenAILangchain:
    def __init__(self):        
        self.chat_completion = AzureChatOpenAI(
            api_key=settings.AZURE_OPENAI_KEY,
            api_version=settings.AZURE_API_VERSION,
            azure_deployment=settings.AZURE_DEPLOYMENT,
            azure_endpoint=settings.AZURE_ENDPOINT,
            temperature=.0,
            max_retries=2,
        )

        self.embedding = AzureOpenAIEmbeddings(
            api_key=settings.AZURE_OPENAI_KEY,
            azure_endpoint=settings.AZURE_ENDPOINT,
            azure_deployment=settings.AZURE_DEPLOYMENT_EMBEDDING,
            openai_api_version=settings.AZURE_API_VERSION,
        )

    def get_embedding(self, message: str):
        '''Get embedding from sentence'''
        return self.embedding.embed_query(message)

    def get_completion(self, messages: list) -> str:
        '''Get completion without function call tools'''
        ai_response = self.chat_completion.invoke(input=messages)
        answer = ai_response.content

        return str(answer)

    def get_chat_tools_completion(self, messages: list) -> BaseMessage:
        '''Get completion alongside function call for getting factual information'''
        self.chat_completion = self.chat_completion.bind_tools(tools=func, tool_choice='auto')
        ai_response = self.chat_completion.invoke(input=messages)

        return ai_response
