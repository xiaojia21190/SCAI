from scholarly import scholarly
import arxiv
from typing import List, Dict
from hashlib import md5
from tenacity import retry, stop_after_attempt, wait_exponential
from autogen import ConversableAgent

from agents.rag.rag_re import index_milvus

import requests


def search_scihub(query: str) -> str:
    search_url = "https://sci-hub.se/"
    payload = {"request": query}
    response = requests.post(search_url, data=payload, allow_redirects=True)

    if response.status_code == 200:
        # document_url = response.url
        return True
    else:
        return False


def filter_papers_by_scihub(papers: list) -> list:
    valid_papers = []

    for paper in papers:
        title = paper.get("title", "")
        result = search_scihub(title)

        # 如果论文在Sci-Hub上找到，则保留
        if result:
            valid_papers.append(paper)

    return valid_papers


def convert_to_list_of_strings(data):
    result = []
    for item in data:
        # 格式化字符串，包含了标题、作者、年份、摘要以及URL等信息
        formatted_str = (
            f"title: {item['title']}\n"
            f"authors: {', '.join(item['authors'])}\n"
            f"published: {item['published']}\n"
            f"abstract: {item['abstract']}\n"
            f"url: {item['url']}\n"
            f"source: {item['source']}\n"
        )
        result.append(formatted_str)
    return result


class PaperMetaSearcher:
    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def search_and_analyze(self, query: str, open) -> str:
        """
        Search and analyze papers

        Args:
            query: Search query

        Returns:
            str: Analysis result
        """
        if not query.strip():
            return "No relevant papers found - empty query"

        # Get the recent papers
        papers = self.get_recent_papers(query, open)

        if not papers:
            return "No relevant papers found"

        # Analyze the papers
        return self.analyze_papers(papers)

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Normalize the title for comparison."""
        return " ".join(title.lower().split())

    @staticmethod
    def _get_paper_hash(title: str, authors: List[str]) -> str:
        """Generate a unique identifier for the paper."""
        content = (
            f"{PaperMetaSearcher._normalize_title(title)}{''.join(sorted(authors))}"
        )
        return md5(content.encode()).hexdigest()

    @staticmethod
    def _search_arxiv(query: str) -> List[Dict]:
        """Search papers from arXiv."""
        papers = []
        try:
            search = arxiv.Search(
                query=query,
                max_results=20,
                sort_by=arxiv.SortCriterion.SubmittedDate,
            )

            for result in search.results():
                papers.append(
                    {
                        "source": "arxiv",
                        "id": result.entry_id,
                        "title": result.title,
                        "authors": [author.name for author in result.authors],
                        "abstract": result.summary,
                        "published": result.published,
                        "url": result.entry_id,
                        "hash": PaperMetaSearcher._get_paper_hash(
                            result.title, [author.name for author in result.authors]
                        ),
                    }
                )
        except Exception as e:
            print(f"arXiv search error: {e}")

        return papers

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _search_scholarly(query: str) -> List[Dict]:
        """Search papers from Google Scholar with retry."""
        papers = []
        try:
            search_query = scholarly.search_pubs(query)
            count = 0

            for result in search_query:
                if count >= 20:
                    break

                # Fetch full information
                try:
                    authors = result.get("bib", {}).get("author", [])
                    if isinstance(authors, str):  # 如果作者是单个字符串
                        authors = [authors]

                    papers.append(
                        {
                            "source": "scholar",
                            "id": result.get("pub_url", ""),
                            "title": result.get("bib", {}).get("title", ""),
                            "authors": authors,
                            "abstract": result.get("bib", {}).get("abstract", ""),
                            "published": result.get("bib", {}).get("pub_year", ""),
                            "url": result.get("pub_url", ""),
                            "hash": PaperMetaSearcher._get_paper_hash(
                                result.get("bib", {}).get("title", ""), authors
                            ),
                        }
                    )
                    count += 1
                except Exception as e:
                    print(f"Error filling scholarly result: {e}")
                    continue

        except Exception as e:
            print(f"Scholarly search error: {e}")

        return papers

    def get_recent_papers(self, query: str, open) -> List[Dict]:
        """Get verified recent papers from arXiv and Google Scholar."""
        arxiv_papers = self._search_arxiv(query)
        # 只查开源，填写OPEN
        # 需要适配一个scihub搜索器，目前还不存在
        # 用一个阴招，用google搜全名，用全名搜scihub
        # 暂时为空，这个可能用本地搜索或者向量数据库更快
        if open == "OPEN":
            scholar_papers = []
            # scholar_papers = self._search_scholarly(query)
            # scholar_papers = filter_papers_by_scihub(scholar_papers)
        else:
            scholar_papers = self._search_scholarly(query)

        print(f"Found {len(arxiv_papers)} papers from arXiv")
        print(f"Found {len(scholar_papers)} papers from Scholar")

        # print(arxiv_papers)
        # print(scholar_papers)

        # De-duplicate using hash as the key
        papers_dict = {}

        for i in range(len(scholar_papers)):
            paper = scholar_papers[i]
            if paper["hash"] not in papers_dict:
                papers_dict[paper["hash"]] = paper

        for i in range(len(arxiv_papers)):
            paper = arxiv_papers[i]
            if paper["hash"] not in papers_dict:
                papers_dict[paper["hash"]] = paper

        # Convert back to list and sort by published date
        papers = list(papers_dict.values())
        papers.sort(key=lambda x: str(x["published"]), reverse=True)

        # 这个地方将会增加一个RAG，用来判断相关性最高的结果
        # 可以用milvus或者llamaindex
        res = index_milvus(convert_to_list_of_strings(papers), query)
        res.sort(key=lambda x: str(x["published"]), reverse=True)

        return res
        # return papers[: self.max_results]

    @staticmethod
    def analyze_papers(papers: List[Dict]) -> str:
        """Analyze papers and generate a report."""
        if not papers:
            return "No relevant papers found in either arXiv or Google Scholar."

        arxiv_papers = [p for p in papers if p["source"] == "arxiv"]
        scholar_papers = [p for p in papers if p["source"] == "scholar"]

        report = f"""Found {len(papers)} relevant papers:
- {len(arxiv_papers)} from arXiv
- {len(scholar_papers)} from Google Scholar

Detailed Analysis:\n\n"""

        for paper in papers:
            report += f"[{paper['source'].upper()}]\n"
            report += f"Title: {paper['title']}\n"
            report += f"Authors: {paper['authors']}\n"
            report += f"ID/URL: {paper['url']}\n"
            report += f"Published: {paper['published']}\n"
            report += f"Abstract: {paper['abstract']}\n\n"

        return report
