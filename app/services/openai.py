import json
import traceback

from langchain_core.messages import HumanMessage, SystemMessage

from app.dependencies import PostgreClient
from app.func_call import FunctionsTools
from app.dependencies import OpenAILangchain

from app.utils import (
    build_context, history_chain_to_string, prepare_answers_to_string
)
from app.config import (
    PERSONA_PROMPT, HYDE_PROMPT, CONTEXT_AWARE_PROMPT,
    ANSWER_ASSESOR_PROMPT
)

class OpenAIServices:
    def __init__(self, history_messages : list = []):
        self.history_messages = history_chain_to_string(history_messages[-10:])
        
        # initiate instance
        self.chat_completion = OpenAILangchain()
        self.pgch_client = PostgreClient()

    def rag_answer(self, sentence):
        '''retrieve augmented generation'''
        new_sentence = self.chat_completion.get_completion(
            messages=[HumanMessage(content=HYDE_PROMPT.format(history_chat=self.history_messages,
                                                              question=sentence))])
        
        embedding_query = self.chat_completion.get_embedding(new_sentence)

        docs = self.pgch_client.get_context(query_embedding=embedding_query,
                                            table_name="foreign_tourists_news",
                                            embedding_col="embedding_news",
                                            threshold=0.7,
                                            n=5)
        
        context_str = build_context(docs)

        messages = [SystemMessage(content=PERSONA_PROMPT)]
        messages.append(HumanMessage(content=CONTEXT_AWARE_PROMPT\
                                     .format(history_chat=self.history_messages, 
                                             context=context_str,
                                             question=sentence)))

        rag_answer = self.chat_completion.get_completion(messages)

        return rag_answer
    
    def assess_answer(self, sentence, answers):
        """Assess which answer is the most relevant"""
        answers_str = prepare_answers_to_string(answers)
        prompt_input = [
            HumanMessage(content=ANSWER_ASSESOR_PROMPT.format(question=sentence, answers=answers_str))
        ]

        ai_result = self.chat_completion.get_completion(prompt_input)

        print(f" > Assess result : {ai_result}")

        answer = answers[int(ai_result) - 1]

        return answer

    def conversation(self, sentence: str):
        """To get response for every query that it get.

        :param session_id:
        :param sentence:
        :return:
        """
        try:
            # try chat gpt openai with tools
            # we used as single message function
            completion = self.chat_completion.get_chat_tools_completion(
                messages=[
                    SystemMessage(content=PERSONA_PROMPT),
                    HumanMessage(content=sentence)])
            
            answers = []
            function_answer = None
            
            if completion.additional_kwargs:
                print(" > Tools are used to answer the question")
                print(completion.additional_kwargs)
                
                # parsing the function call name
                function = completion.additional_kwargs["tool_calls"][0]['function']
                fn_name = function["name"]
                kwarg = json.loads(function["arguments"])

                # get the function as a function object
                function = getattr(FunctionsTools(), fn_name)

                # call the function with params if there is params
                # otherwise don't call it
                function_answer = function(**kwarg) if kwarg else function()

                print(f" > Function answer : {function_answer}")
                answers.append(function_answer)
            
            try:
                # retrieved augmented generation (RAG) flow
                print(" > Try RAG answer")
                rag_answer = self.rag_answer(sentence)

                print(f" > RAG answer : {rag_answer}")
                answers.append(rag_answer)

            except:
                rag_answer = completion.content

            if len(answers) == 2:
                print(" > Ada dua jawaban")
                answer = self.assess_answer(sentence=sentence, answers=answers)
                return answer
            
            elif function_answer is None:
                print(" > Function call tidak terpanggil")
                return rag_answer
            
            elif function_answer is not None:
                return function_answer
            
            return answer

        except Exception as e:
            traceback.print_exc()

            return "Mohon maaf saat ini chatbot sedang ada gangguan, mohon tunggu beberapa saat lagi yaa..."
