from app.services.retriever import retrieve
from app.services.generator import generate_answer
from app.services.memory import get_history, update_history

GREETINGS = {"hi", "hello", "hey", "hai", "hii", "good morning", "good afternoon", "good evening"}


def is_greeting(query: str) -> bool:
    return query.lower().strip(" .,!?\t\r\n") in GREETINGS


def rag_pipeline(query: str):
    query = query.strip()
    if not query:
        return {"answer": "Please enter a question.", "contexts": []}

    if is_greeting(query):
        answer = (
            "Welcome to our customer support chat. How can I assist you today?\n\n"
            "You might want to ask:\n"
            "- About your order status\n"
            "- A question about our products or services\n"
            "- A query about our business hours"
        )
        update_history(query, answer)
        return {"answer": answer, "contexts": []}

    contexts = retrieve(query)
    history = get_history()

    answer = generate_answer(query, contexts, history)

    update_history(query, answer)

    return {"answer": answer, "contexts": contexts}
