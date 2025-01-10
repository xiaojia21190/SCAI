# import os
# from llama_index.core import (
#     VectorStoreIndex,
#     SimpleDirectoryReader,
#     Settings,
#     StorageContext,
#     load_index_from_storage,
#     get_response_synthesizer,
#     chat_engine,
# )
# from llama_index.core.memory import ChatMemoryBuffer
# from llama_index.llms.ollama import Ollama
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.readers.file import PDFReader
# from llama_index.core.retrievers import VectorIndexRetriever
# from llama_index.core.query_engine import RetrieverQueryEngine
# from llama_index.core import PromptTemplate


# # 使用创建的索引执行查询
# def persist(file_path: str, index_dir: str):
#     # load pdf
#     documents = SimpleDirectoryReader(file_path).load_data()

#     # TODO 需要考虑什么样的模型/Embedding模型更好
#     # emb
#     Settings.embed_model = OllamaEmbedding(model_name="b  ")

#     # llm
#     Settings.llm = Ollama(model="gemma2:2b", request_timeout=360)

#     # IN THE TEST, THE DATA SHALL NOT BE PERSIST
#     index = VectorStoreIndex.from_documents(documents)
#     index.storage_context.persist(persist_dir=index_dir)


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
    get_response_synthesizer,
    chat_engine,
)
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PDFReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import PromptTemplate
from llama_index.vector_stores.faiss import FaissVectorStore

import faiss

# res = faiss.StandardGpuResources()

# # build a flat (CPU) index
# index_flat = faiss.IndexFlatL2(d)
# # make it into a gpu index
# gpu_index_flat = faiss.index_cpu_to_gpu(res, 0, index_flat)


# define embedding function
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# llm
Settings.llm = Ollama(model="llama3.2:3b-instruct-q8_0", request_timeout=360)

embeddings = OllamaEmbedding(model_name="nomic-embed-text")

single_vector = embeddings.get_query_embedding("this is some text data")


faiss_index = faiss.IndexFlatL2(len(single_vector))

print(len(single_vector))

documents = SimpleDirectoryReader("scai_rag/doc").load_data()

vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

index.storage_context.persist("scai_rag/db_faiss")

# load index from disk
# vector_store = FaissVectorStore.from_persist_dir("scai_rag/db_test")
# storage_context = StorageContext.from_defaults(
#     vector_store=vector_store, persist_dir="scai_rag/db_test"
# )
# index = load_index_from_storage(storage_context=storage_context)

# https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/
# query_engine = index.as_query_engine()
# response = query_engine.query("is there any paper about computer science")
# print(response)

# persist("scai_rag/doc", "scai_rag/db_arxiv")


import logging
import sys

# Uncomment to see debug logs
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
