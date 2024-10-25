def build_context(context_docs: list = []):
    """Build context from list to string"""
    return "\n".join([doc[6] for doc in context_docs])

def history_chain_to_string(history_chat : list = []) -> str:
    """Convert history chat to string type"""
    return "\n".join(f"{str(doc.type).capitalize()} : {doc.content}" for doc in history_chat)

def prepare_answers_to_string(answers_list : list = []) -> str:
    """Prepare answers from list to string"""
    return "\n".join([ f"{i+1}) {doc}" for i, doc in enumerate(answers_list)])