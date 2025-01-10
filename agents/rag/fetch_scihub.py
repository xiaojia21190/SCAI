import asyncio
import os
from pathlib import Path
import re
import requests
from pypdf import PdfReader  # 使用 pypdf 进行 PDF 文本提取
from urllib.request import urlretrieve
from config import DOC_DIR, PDF_DIR


async def arxiv_scraper(aid, file_path):
    print("arxiv 开始下载", aid)
    flag = True
    url = f"https://arxiv.org/pdf/{aid}"

    try:
        urlretrieve(url, file_path)
        flag = True
    except Exception as e:
        print(f"arxiv 下载失败: {e}")
        flag = False

    return flag


async def scihub_scraper(doi, url, file_path):
    flag = True
    print("scihub 开始下载", doi)
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # 查找 <embed type="application/pdf" ... src="URL"> 的模式
        pattern = re.compile(
            r'<embed[^>]*type="application\/pdf"[^>]*src="([^"]+)"[^>]*>', re.IGNORECASE
        )

        match = pattern.search(html_content)

        if match:
            pdf_url = match.group(1)
            print("PDF URL: http:", pdf_url)
            # 下载PDF文件
            urlretrieve(f"http:{pdf_url}", file_path)
        else:
            print("未找到匹配的 <embed> 标签")
            return False

    except requests.exceptions.RequestException as e:
        print(f"请求网页时发生错误： {e}")
        return False

    except Exception as e:
        print(f"发生意外错误： {e}")
        return False


def convert_pdf_to_txt(pdf_path, txt_path):
    print(f"正在转换 {pdf_path} 到 {txt_path}")
    try:
        # 使用 PyPDF2 读取 PDF 文件
        reader = PdfReader(pdf_path)
        text = ""

        # 提取每一页的文本
        for page in reader.pages:
            text += page.extract_text()

        # 将提取的文本写入 TXT 文件
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        print(f"转换完成： {txt_path}")
        return True
    except Exception as e:
        print(f"PDF 转换失败: {e}")
        return False


def scraper(doi, aid):
    # 创建文件夹
    Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
    Path(DOC_DIR).mkdir(parents=True, exist_ok=True)

    # 文件路径设置
    aid = aid.replace("/", "%2F")
    pdf_path = os.path.join(PDF_DIR, f"{aid}.pdf")
    txt_path = os.path.join(DOC_DIR, f"{aid}.txt")

    # 检查文件是否已存在
    if os.path.exists(pdf_path):
        print(f"文件 {pdf_path} 已存在")
    else:
        # arxiv 下载
        arxiv_success = asyncio.run(arxiv_scraper(aid, pdf_path))
        if not arxiv_success:
            # 如果 arxiv 下载失败，尝试 sci-hub 下载
            scihub_url = f"https://sci-hub.se/{doi}"
            asyncio.run(scihub_scraper(doi, scihub_url, pdf_path))

    # 如果 PDF 文件已下载，开始转换
    if os.path.exists(pdf_path):
        if not os.path.exists(txt_path):  # 如果 TXT 文件还未生成
            convert_pdf_to_txt(pdf_path, txt_path)
        else:
            print(f"文件 {txt_path} 已存在")


scraper("10.1017", "10.1017/s0263574718001145")
