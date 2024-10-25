from langchain.schema import HumanMessage, SystemMessage
from app.dependencies.OpenAI import OpenAILangchain
from app.dependencies.Postgre import get_one_answer, get_top_3_similar_answer
from app.rag.faq import FAQ
