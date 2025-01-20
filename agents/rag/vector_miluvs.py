from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.milvus import MilvusVectorStore
from IPython.display import Markdown, display

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from pymilvus import MilvusClient
from pymilvus import model
import ollama
from glob import glob
from tqdm import tqdm


def emb_text(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


# scai_rag/test/*.json
# True 建立向量数据库 False查询
def train(file_dir: str):

    client = MilvusClient("http://localhost:19530")
    collection_name = "rag_test"

    text_lines = []

    for file_path in glob(file_dir, recursive=True):
        with open(file_path, "r") as file:
            file_text = file.read()

        # 按行分割，并将每一行添加到 text_lines 列表
        text_lines += file_text.splitlines()

    if client.has_collection(collection_name=collection_name):
        client.drop_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        dimension=768,  # The vectors we will use in this demo has 768 dimensions
        metric_type="IP",  # Inner product distance
        consistency_level="Strong",  # Strong consistency level
    )

    data = []

    for i, line in enumerate(tqdm(text_lines, desc="SCAI")):
        data.append({"id": i, "vector": emb_text(line), "text": line})

    client.insert(collection_name=collection_name, data=data)

    search_res = client.search(
        collection_name=collection_name,
        data=[
            emb_text("Redundancy Hierarchy")
        ],  # Use the `emb_text` function to convert the question to an embedding vector
        limit=3,  # Return top 3 results
        search_params={"metric_type": "IP", "params": {}},  # Inner product distance
        output_fields=["text"],  # Return the text field
    )
    print(search_res)


train()
