import os
from pypdf import PdfReader
import requests

from agents.rag.config import (
    INIT_MEM_RAG_QUERY,
    PDF_DIR,
    DOC_DIR,
)
from agents.rag.rag import chat_rag
from agents.rag.rag import chat_rag_init
from agents.rag.fetch_arxiv import PaperSearcher


pdf_dir = PDF_DIR
doc_dir = DOC_DIR

# 创建保存PDF和文档的文件夹（如果不存在）
os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(doc_dir, exist_ok=True)


def download_pdf(arxiv_id, pdf_dir):
    # 构建arxiv PDF下载URL
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # 设置本地文件路径
    pdf_path = os.path.join(pdf_dir, f"{arxiv_id}.pdf")

    # 下载PDF文件
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(pdf_path, "wb") as file:
            file.write(response.content)
        print(f"PDF 下载成功: {pdf_path}")
    else:
        print(f"无法下载PDF: {pdf_url}")
        return None
    return pdf_path


def convert_pdf_to_text(pdf_path):
    # 使用PyPDF2读取PDF文件并提取文本
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def save_text_to_file(text, arxiv_id, doc_dir):
    # 将文本保存到指定目录
    text_path = os.path.join(doc_dir, f"{arxiv_id}.txt")
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"文本文件保存成功: {text_path}")


def rag_proces(res, arxiv_ids, pdf_dir, doc_dir, query):
    # 存储所有生成的文档路径
    doc_files = []
    titles = []

    # 遍历所有arxiv_id
    for arxiv_id in arxiv_ids:
        # 构造PDF和TXT文件的路径
        pdf_path = os.path.join(pdf_dir, f"{arxiv_id}.pdf")
        txt_path = os.path.join(doc_dir, f"{arxiv_id}.txt")

        # 检查PDF文件是否存在，如果不存在则下载
        if not os.path.exists(pdf_path):
            pdf_path = download_pdf(arxiv_id, pdf_dir)
            if not pdf_path:
                print(f"Failed to download PDF for {arxiv_id}. Skipping...")
                continue  # 如果下载失败，跳过此篇文章
        else:
            print(f"PDF for {arxiv_id} already exists, skipping download.")

        # 如果PDF下载成功且TXT文件不存在，进行转换
        if pdf_path and not os.path.exists(txt_path):
            text = convert_pdf_to_text(pdf_path)

            # 保存文本到文件
            save_text_to_file(text, arxiv_id, doc_dir)
            print(f"Text file for {arxiv_id} saved.")
        elif os.path.exists(txt_path):
            print(f"Text file for {arxiv_id} already exists, skipping conversion.")

        # 将生成的TXT文件路径添加到doc_files列表中
        doc_files.append(f"{doc_dir}/{arxiv_id}.txt")

    for item in res:
        titles.append(f"{item['title']}")

    # 将文档路径列表传递给chat_rag_init
    chat_engine = chat_rag_init(
        f"{INIT_MEM_RAG_QUERY}, the paper in your memory are: {titles}", doc_files
    )

    init_chat = chat_rag(
        chat_engine, "list the paper in your memory, and give a clear, simple abstract"
    )
    print(" ")
    print(f"{init_chat}")

    res = chat_rag(chat_engine, query)
    return res

    # print(" ")
    # print("Chat engine initialized. You can now ask questions.")
    # print("Type 'exit' to quit the program.\n")

    # # 多轮对话
    # while True:
    #     user_input = input("You: ")  # 接受用户输入
    #     if user_input.lower() == "exit":
    #         print("Exiting the chat. Goodbye!")
    #         break  # 用户输入 'exit' 时退出

    #     # 使用 chat_rag 处理用户问题
    #     response = chat_rag(chat_engine, user_input)
    #     print(" ")
    #     print(f"ChatRAG: {response}")
    #     print(" ")


def run_arxiv_rag(query: str, max_results=5):

    searcher = PaperSearcher()

    # 搜索论文（例如搜索“machine learning”）
    res = searcher._search_arxiv(query, max_results=max_results)

    arxiv_ids = []

    # 遍历解析后的数据，收集所有的 arxiv_id
    for item in res:
        print(f"ID: {item['aid']}, Name: {item['title']}")
        arxiv_ids.append(item["aid"])

    # 调用 rag_proces 函数处理所有的 arxiv_id
    rag_proces(res, arxiv_ids, pdf_dir, doc_dir, query)


# run_arxiv_rag("Find me some paper about RAG")

# phi4
# reply, mentioned, search big V
# {
#     "abstract": "BitVM2 is a novel paradigm that enables arbitrary program execution in Bitcoin, thereby combining Turing-complete expressiveness with the security of Bitcoin consensus. At its core, BitVM2 leverages optimistic computation, assuming operators are honest unless proven otherwise by challengers through fraud proofs, and SNARK proof verification scripts, which are split into sub-programs that are executed within Bitcoin transactions. As a result, BitVM2 ensures program correctness with just three on-chain transactions. BitVM2 significantly improves over prior BitVM designs by enabling, for the first time, permissionless challenging and by reducing the complexity and number of on-chain transactions required to resolve disputes. Our construction requires no consensus changes to Bitcoin. BitVM2 enables the design of an entirely new class of applications in Bitcoin. We showcase that by presenting BitVM Bridge, a protocol that enhances prior Bitcoin bridges by reducing trust assumptions for the safety of deposits from an honest majority (t-of-n) to existential honesty (1-of-n) during setup. To guarantee liveness, we only require one active rational operator (while the others can be malicious). Any user can act as challenger, facilitating permissionless verification of the protocol.",
#     "title": "BitVM2: Bridging Bitcoin to Second Layers",
#     "author": "Robin Linus, Lukas Aumayr, Alexei Zamyatin, Andrea Pelosi, Zeta Avarikioti, Matteo Maffei",
#     "doi": "2405.06842"
# }

# ollama run phi3:14b
