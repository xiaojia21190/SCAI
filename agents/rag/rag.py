import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
    chat_engine,
)
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import PromptTemplate
from llama_index.embeddings.openai import OpenAIEmbedding
from openai import OpenAI

from config.llm_config import LLM_CONFIG, MODEL


# 使用创建的索引执行查询
def query_rag(
    query: str, prompt: str, doc_dir: str, index_dir: str, temp_or_presist: str
):
    # load pdf

    if MODEL == "GPT":
        Settings.embed_model = OpenAIEmbedding(api_key=LLM_CONFIG["api_key"])
    else:
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # llm
    if MODEL == "GPT":
        Settings.llm = OpenAI(
            api_key=LLM_CONFIG["api_key"], temperature=0, model=LLM_CONFIG["model"]
        )
    else:
        Settings.llm = Ollama(model="gemma2:2b", request_timeout=360)

    # IN THE TEST, THE DATA SHALL NOT BE PERSIST
    if temp_or_presist == "TEMP":
        documents = SimpleDirectoryReader(doc_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=index_dir)

    else:
        print("from default?")
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        print("load index?")
        index = load_index_from_storage(storage_context)

    # retriever = VectorIndexRetriever(
    #     index=index,
    #     similarity_top_k=2,
    # )

    # # configure response synthesizer
    # response_synthesizer = get_response_synthesizer()

    # query_engine = RetrieverQueryEngine(
    #     retriever=retriever,
    #     response_synthesizer=response_synthesizer,
    # )
    query_engine = index.as_query_engine(response_mode="tree_summarize")
    new_summary_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        f"{prompt}"
        "Query: {query_str}\n"
        "Answer: "
    )
    new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
    query_engine.update_prompts(
        {"response_synthesizer:summary_template": new_summary_tmpl}
    )

    try:
        response = query_engine.query(query)
        return str(response)  # 返回查询结果
    except Exception as e:
        return f"Error during query: {str(e)}"


def chat_rag_init(prompt: str, doc: str):
    documents = SimpleDirectoryReader(input_files=doc).load_data()

    if MODEL == "GPT":
        Settings.embed_model = OpenAIEmbedding(api_key=LLM_CONFIG["api_key"])
    else:
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # llm
    if MODEL == "GPT":
        Settings.llm = OpenAI(
            api_key=LLM_CONFIG["api_key"], temperature=0, model=LLM_CONFIG["model"]
        )
    else:
        Settings.llm = Ollama(model="gemma2:2b", request_timeout=360)

    # IN THE TEST, THE DATA SHALL NOT BE PERSIST
    index = VectorStoreIndex.from_documents(documents)

    # # configure retriever
    # retriever = VectorIndexRetriever(
    #     index=index,
    #     similarity_top_k=2,
    # )

    # # configure response synthesizer
    # response_synthesizer = get_response_synthesizer()

    memory = ChatMemoryBuffer.from_defaults(token_limit=2000)

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(prompt),
    )

    return chat_engine


def chat_rag(chat_engine: chat_engine.ContextChatEngine, query: str):
    try:
        response = chat_engine.chat(query)
        return str(response)  # 返回查询结果
    except Exception as e:
        return f"Error during query: {str(e)}"
