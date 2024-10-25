from app.rag import *

class FAQ:
    def __init__(self, sentence: str, chains: list, persona: list):
        self.OAI_instance = OpenAILangchain()
        self.sentence = sentence
        self.CA_Question = sentence
        self.chains = chains
        self.related_docs = []
        self.persona = persona

    def is_faq(self):
        self.related_docs = get_one_answer(self.OAI_instance.get_embeddings(self.sentence))
        print(self.related_docs)

        return len(self.related_docs) > 0

    def is_HyDE(self):
        # TODO Modularize hyde and ca prompt

        CA_PROMPT = f"""
Given previous chat chains and this follow up input, try to understand user intent and rephrase the Follow Up Input to be a standalone question/instruction.
Don't clarify the question.        
Follow Up Input: {self.sentence}        
Standalone Question Concisely in Indonesian:"""
        # print(f"sentence : {self.sentence}")
        # print(f"chains : {self.chains}")
        self.chains.append(HumanMessage(content=self.sentence, ))
        self.chains.append(SystemMessage(content=CA_PROMPT, ))
        question = self.OAI_instance.get_completion(self.chains)
        self.CA_Question = question
        print(f"CA question : {question}")
        # print(f"question : {question}"

        HA_INPUT = f""" Generate a hypothetical answer to the user_question don't use any actual facts. 
NEVER say you Don't know the answer. Pretend you know everything about Nawatech.
user_question: {self.CA_Question}

Hypothetical_Answer:"""
        HA_prompts = self.persona + [SystemMessage(content=HA_INPUT, )]

        hypo_answer = self.OAI_instance.get_completion(HA_prompts)

        print(f"hypo_answer : {hypo_answer}")

        related_docs = get_top_3_similar_answer(self.OAI_instance.get_embeddings(hypo_answer))
        print(f"docs : {related_docs}")
        self.related_docs = "\n".join([doc[1] for doc in related_docs])
        print(f"related_docs : {self.related_docs}")
        print(related_docs)

        return len(related_docs) > 0

    def get_answer_from_qustion(self):
        print(self.related_docs)
        # hati-hati sama prompt ini
        prompt = f"""Use the following pieces of FAQ_Answer to help you answer the Question.
        FAQ_Answer  : \"{self.related_docs[0][0]}\".
        Question : \"{self.sentence}\"
        Answer it straight to the point format the answer to be as neat as possible, consider spacing and new lines.
        Retain the information as much as possible.
        Answer in indonesian: 
        """

        naive_prompt = self.persona + [SystemMessage(content=prompt, )]
        response = self.OAI_instance.get_completion(naive_prompt)
        print(f"response : {response}")

        return response

    def get_answer(self):
        refine = f"""Your job is to answer user_question given FAQ_passages .

You Must follow this task Description ton answer the user_question.

Task Description below:
1. Read the given user_question and three from FAQ documents to gather relevant information.
2. Write reading notes summarizing the key points from these FAQ documents.
3. Discuss the relevance of the given question and and FAQ documents.
4. If some passages are relevant to the given question, provide a brief answer based on the passages.
5. If no passage is relevant, direcly provide answer without considering the passages from FAQ Documents.

FAQ_passages : \"{self.related_docs}\".
user_question : \"{self.CA_Question}\"
Answer concisely Indonesian: """

        prompts = self.persona + [SystemMessage(content=refine, )]

        faq_response = self.OAI_instance.get_completion(prompts)

        return faq_response
