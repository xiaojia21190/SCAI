from glob import glob
import re
from llama_index.core.schema import TextNode
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
    chat_engine,
)
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama
from pymilvus import MilvusClient

from config.llm_config import MODEL
import json
import ast


def emb_text(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


def convert_to_json(data):
    parsed_data = []

    for sublist in data:
        for item in sublist:
            # Extract the 'text' part and treat it as a single string
            entity_text = item.get("entity", {}).get("text", "")

            # Convert the text to a single string (handling escape sequences)
            entity_text = entity_text.replace(
                "\\n", "\n"
            )  # Replace the escaped newline with actual newline

            # Create a dictionary to hold the parsed fields
            parsed_dict = {}

            # Split the text based on actual newline
            lines = entity_text.split("\n")

            # Process each line to extract key-value pairs
            for line in lines:
                line = line.strip()  # Remove any extra spaces
                if line:
                    match = re.match(r"([A-Za-z ]+): (.+)", line)
                    if match:
                        key, value = match.groups()
                        parsed_dict[key.strip()] = value.strip()

            # Add the parsed dictionary to the result
            parsed_data.append(parsed_dict)

    return parsed_data


def index_milvus(docs: list, query: str):

    client = MilvusClient("http://localhost:19530")
    collection_name = "rag_0_temp"

    if client.has_collection(collection_name=collection_name):
        client.drop_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        dimension=768,  # The vectors we will use in this demo has 768 dimensions
        metric_type="IP",  # Inner product distance
        consistency_level="Strong",  # Strong consistency level
    )

    data = [
        {"id": i, "vector": emb_text(docs[i]), "text": docs[i], "subject": "history"}
        for i in range(len(docs))
    ]

    client.insert(collection_name=collection_name, data=data)

    search_res = client.search(
        collection_name=collection_name,
        data=[
            emb_text(query)
        ],  # Use the `emb_text` function to convert the question to an embedding vector
        limit=3,  # Return top 3 results
        search_params={"metric_type": "IP", "params": {}},  # Inner product distance
        output_fields=["text"],  # Return the text field
    )
    res = convert_to_json(search_res)
    print(res)
    return res


def index_paper(paper: list, query: str):

    if MODEL != "GPT":
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # llm
    if MODEL != "GPT":
        Settings.llm = Ollama(model="gemma2:2b", request_timeout=360)

    # 将 paper 列表中的每个元素转化为一个 SimpleNode
    nodes = [TextNode(text=content) for content in paper]

    # 创建索引
    index = VectorStoreIndex(nodes)

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    # 进行查询
    query = "What is the second paper about?"
    response = query_engine.query(query)

    # 输出查询结果
    print(response)


# # 示例调用
# data = ['[{\'id\': 103, \'distance\': 247.26255798339844, \'entity\': {\'text\': \'{"abstract": "  We study the existence of soliton and black hole solutions of\\\\nfour-dimensional su(N) Einstein-Yang-Mills theory with a negative cosmological\\\\nconstant. We prove the existence of non-trivial solutions for any integer N,\\\\nwith N-1 gauge field degrees of freedom. In particular, we prove the existence\\\\nof solutions in which all the gauge field functions have no zeros. For fixed\\\\nvalues of the parameters (at the origin or event horizon, as applicable)\\\\ndefining the soliton or black hole solutions, if the magnitude of the\\\\ncosmological constant is sufficiently large, then the gauge field functions all\\\\nhave no zeros. These latter solutions are of special interest because at least\\\\nsome of them will be linearly stable.\\\\n", "title": "On the existence of soliton and hairy black hole solutions of su(N)\\\\n  Einstein-Yang-Mills theory with a negative cosmological constant", "authors": "J. E. Baxter and Elizabeth Winstanley", "doi": "10.1088/0264-9381/25/24/245014", "aid": "0808.2977"},\'}}, {\'id\': 619, \'distance\': 246.86395263671875, \'entity\': {\'text\': \'{"abstract": "  Growth of massive black holes (MBHs) in galactic centers comes mainly from\\\\ngas accretion during their QSO/AGN phases. In this paper we apply an extended\\\\nSoltan argument, connecting the local MBH mass function with the time-integral\\\\nof the QSO luminosity function, to the demography of MBHs and QSOs from recent\\\\noptical and X-ray surveys, and obtain robust constraints on the luminosity\\\\nevolution (or mass growth history) of individual QSOs (or MBHs). We find that\\\\nthe luminosity evolution probably involves two phases: an initial exponentially\\\\nincreasing phase set by the Eddington limit and a following phase in which the\\\\nluminosity declines with time as a power law (with a slope of -1.2--1.3) set by\\\\na self-similar long-term evolution of disk accretion. Neither an evolution\\\\ninvolving only the increasing phase with a single Eddington ratio nor an\\\\nexponentially declining pattern in the second phase is likely. The period of a\\\\nQSO radiating at a luminosity higher than 10% of its peak value is about\\\\n(2-3)x10^8 yr, during which the MBH obtains ~80% of its mass. The\\\\nmass-to-energy conversion efficiency is $0.16\\\\\\\\pm0.04 ^{+0.05}_{-0}$, with the\\\\nlatter error accounting for the maximum uncertainty due to Compton-thick AGNs.\\\\nThe expected Eddington ratios in QSOs from the constrained luminosity evolution\\\\ncluster around a single value close to 0.5-1 for high-luminosity QSOs and\\\\nextend to a wide range of lower values for low-luminositycertainty due to Compton-thick AGNs.\\\\nThe expected Eddington ratios in QSOs from the constrained luminosity evolution\\\\ncluster around a single value close to 0.5-1 for high-luminosity QSOs and\\\\nextend to a wide range of lower values for low-luminosity ones. The Eddington\\\\nratios for high luminosity QSOs appear to conflict with those estimated from\\\\nobservations (~0.25) by using some virial mass estimators for MBHs in QSOs\\\\nunless the estimators systematically over-estimate MBH masses by a factor of\\\\n2-4. We also infer the fraction of optically obscured QSOs ~60-80%. Further\\\\napplications of the luminosity evolution of individual QSOs are also discussed.\\\\n", "title": "Toward precise constraints on growth of massive black holes", "authors": "Qingjuan Yu, Youjun Lu", "doi": "10.1086/592770", "aid": "0808.3777"},\'}}, ...']

# # 调用函数
# json_output = convert_to_json(data)

# # 打印结果
# print(json_output)
