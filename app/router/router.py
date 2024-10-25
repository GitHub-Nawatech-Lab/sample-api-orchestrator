import traceback

from fastapi import APIRouter
from fastapi import Query
from app.schemas import *
from app.router.auth import ApiKeyMiddleware
from app.services.openai import OpenAIServices
from langchain_community.chat_message_histories import (
    PostgresChatMessageHistory,
)
from langchain_core.messages import AIMessage, HumanMessage

from app.schemas.params import SentenceInput, RoomIdInput

from app.settings import settings


router = APIRouter(route_class=ApiKeyMiddleware)


@router.post("/conversation", openapi_extra={"security": [{"ApiKeyAuth": []}]})
async def gpt_conversation(input_payload : SentenceInput):
    '''This route is for gpt based conversatoin'''
    input_dict = input_payload.model_dump(mode="python")

    session_id = input_dict.get("session_id")
    sentence = input_dict.get("sentence")

    pgch_client = PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=settings.POSTGRE_CONNECTION_STR
    )

    # get history chat
    history_chat = pgch_client.messages
    openai_service = OpenAIServices(history_messages=history_chat)

    try:
        # ai conversation result
        result = openai_service.conversation(sentence=sentence,)

        # submit chat history
        message_list = [HumanMessage(content=sentence), AIMessage(content=result)]
        pgch_client.add_messages(message_list)
        
        return success_handler(data=result)
    
    except Exception as e:
        traceback.print_exc()
        return error_handler()


@router.post("/clear-history", openapi_extra={"security": [{"ApiKeyAuth": []}]})
async def clear_history(room_id_payload : RoomIdInput):
    '''This route is to clear chat history'''
    room_id_dict = room_id_payload.model_dump(mode="python")
    session_id = room_id_dict.get("session_id")


    pgch_client = PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=settings.POSTGRE_CONNECTION_STR
    )

    pgch_client.clear()

    payload_output = {
        "session_id" : session_id,
        "deleted" : True
    }
    
    return success_handler(data=payload_output)
