PERSONA_PROMPT = """Your name is \"Halina\". 
You are an Hackathon helpful assistant.
You can only answer about Indonesian tourism.
Your answer must be in Indonesian language."""

CONTEXT_AWARE_PROMPT = """Please answer the following user question based on the relevant provided context. If the question is not clear, use previous chat chains for context. Answer in a straight forward manner. If the question is outside of the scope then says that your information is limited by Indonesian tourism knowledge.

History : {history_chat}

Context : {context}

Question : {question}
Answer:"""

HYDE_PROMPT = """Please write a news passage to answer the following question in one sentence. You can use history chat to improve the answer.

History : {history_chat}

Question: {question}
Passage:"""

ANSWER_ASSESOR_PROMPT = """I want you to act as an answer assessor. I will provide multiple answers to a question, and your task is to assess which answer is the most relevant to the question. You should respond with the number or label of the most relevant answer, and nothing else. Do not provide any explanations or reasoning for your choice. My first question is: "{question}" and here are the answers: {answers}."""