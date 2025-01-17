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
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

from llama_index.core.tools import QueryEngineTool, ToolMetadata


# 使用创建的索引执行查询
def query_rag(
    query: str, prompt: str, doc_dir: str, index_dir: str, temp_or_presist: str
):
    # load pdf

    embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # llm
    llm = Ollama(model="gemma2:2b", request_timeout=360)

    Settings.embed_model = embed_model
    Settings.llm = llm
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

    # 工具的metadata, prompt很重要, 写的不对，就会发癫
    query_engine_tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="scihub_info",
                description=("Provides information about scihub."),
            ),
        )
    ]

    agent = ReActAgent.from_tools(
        query_engine_tools,
        llm=llm,
        verbose=True,
        # context=context
    )
    try:
        response = agent.chat(query)
        return str(response)  # 返回查询结果
    except Exception as e:
        return f"Error during query: {str(e)}"


query_rag(
    "What is the total size of Sci-Hub database In Chemistry",
    "",
    "test",
    "test/db",
    "TEMP",
)
