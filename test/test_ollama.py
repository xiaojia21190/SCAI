import ollama


def chat_intent(query: str) -> str:

    # Use Ollama to get a response based on initial memory
    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {
                "role": "user",
                "content": query,
            },
        ],
    )
    return response["message"]["content"]
    

print(chat_intent("hah"))
