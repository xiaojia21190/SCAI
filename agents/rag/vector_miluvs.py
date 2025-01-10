from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.milvus import MilvusVectorStore
from IPython.display import Markdown, display

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import textwrap
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from pymilvus import MilvusClient
from pymilvus import model


# True 建立向量数据库 False查询
def train(flag: bool):
    # define embedding function
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # llm
    Settings.llm = Ollama(model="gemma2:2b", request_timeout=360)

    # training
    if flag:
        embedding_fn = model.DefaultEmbeddingFunction()

        client = MilvusClient("http://localhost:19530")
        # Insert more docs in another subject.
        docs = [
            "Machine learning has been used for drug design.",
            "Computational synthesis with AI algorithms predicts molecular properties.",
            "DDR1 is involved in cancers and fibrosis.",
        ]
        vectors = embedding_fn.encode_documents(docs)
        data = [
            {"id": 3 + i, "vector": vectors[i], "text": docs[i], "subject": "biology"}
            for i in range(len(vectors))
        ]

        client.insert(collection_name="llamacollection", data=data)

        # This will exclude any text in "history" subject despite close to the query vector.
        res = client.search(
            collection_name="llamacollection",
            data=embedding_fn.encode_queries(["tell me black hole related information"]),
            limit=10,
            output_fields=["text", "subject"],
        )

        print(res)

        # vector_store = MilvusVectorStore(
        #     uri="http://localhost:19530", dim=768, overwrite=False
        # )
        # documents = SimpleDirectoryReader(
        #     input_files=["scai_rag/doc/split_file_3.txt"]
        # ).load_data()
        # storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # index = VectorStoreIndex.from_documents(
        #     documents, storage_context=storage_context
        # )
    else:
        vector_store = MilvusVectorStore(
            uri="http://localhost:19530", dim=768, overwrite=True
        )
        documents = SimpleDirectoryReader(
            input_files=["scai_rag/test/test.json"]
        ).load_data()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )

        query_engine = index.as_query_engine(response_mode="tree_summarize")

        embedding_fn = model.DefaultEmbeddingFunction()
        embeddings = OllamaEmbedding(model_name="nomic-embed-text")
        single_vector = embedding_fn.encode_queries(
            ["tell me something about black holes"]
        )

        client = MilvusClient("http://localhost:19530")

        res1 = client.search(
            collection_name="llamacollection",  # target collection
            data=single_vector,  # query vectors
            limit=10,  # number of returned entities
            output_fields=["text", "subject"],  # specifies fields to be returned
        )

        print(res1)

        res2 = query_engine.query("tell me something about black holes")
        print(res2)


train(False)
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/MilvusIndexDemo/
