from scholarly import scholarly
import arxiv
from typing import List, Dict
from hashlib import md5
from tenacity import retry, stop_after_attempt, wait_exponential
from autogen import ConversableAgent

current_papers = []


def search_and_analyze(query: str, max_results: int = 5) -> str:
    """
    搜索并分析论文

    Args:
        query: 搜索查询
        max_results: 最大结果数量

    Returns:
        str: 分析结果
    """
    if not query.strip():
        return "No relevant papers found - empty query"

    # 获取最新论文
    papers = get_recent_papers(query, max_results)

    if not papers:
        return "No relevant papers found"

    # 分析论文
    return analyze_papers(papers)


def _normalize_title(title: str) -> str:
    """标准化标题以便比较"""
    return " ".join(title.lower().split())


def _get_paper_hash(title: str, authors: List[str]) -> str:
    """生成论文的唯一标识"""
    content = f"{_normalize_title(title)}{''.join(sorted(authors))}"
    return md5(content.encode()).hexdigest()


def _search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    """从 arXiv 搜索论文"""
    papers = []
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
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
                    "hash": _get_paper_hash(
                        result.title, [author.name for author in result.authors]
                    ),
                }
            )
    except Exception as e:
        print(f"arXiv search error: {e}")

    return papers


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def _search_scholarly(query: str, max_results: int = 5) -> List[Dict]:
    """从 Google Scholar 搜索论文，带重试机制"""
    papers = []
    try:
        search_query = scholarly.search_pubs(query)
        count = 0

        for result in search_query:
            if count >= max_results:
                break

            # 获取完整信息
            try:
                pub = scholarly.fill(result)
                authors = [author.get("name", "") for author in pub.get("authors", [])]

                papers.append(
                    {
                        "source": "scholar",
                        "id": pub.get("pub_url", ""),
                        "title": pub.get("title", ""),
                        "authors": authors,
                        "abstract": pub.get("abstract", ""),
                        "published": pub.get("year", ""),
                        "url": pub.get("pub_url", ""),
                        "hash": _get_paper_hash(pub.get("title", ""), authors),
                    }
                )
                count += 1
            except Exception as e:
                print(f"Error filling scholarly result: {e}")
                continue

    except Exception as e:
        print(f"Scholarly search error: {e}")

    return papers


def get_recent_papers(query: str, max_results: int = 5) -> List[Dict]:
    """获取经过验证的最新论文，确保两个来源都被使用"""
    # 每个源获取 max_results 个结果
    arxiv_papers = _search_arxiv(query, max_results)
    scholar_papers = _search_scholarly(query, max_results)

    print(f"Found {len(arxiv_papers)} papers from arXiv")
    print(f"Found {len(scholar_papers)} papers from Scholar")

    # 使用字典去重，以 hash 为键
    papers_dict = {}

    # 交替添加两个来源的论文，确保均衡
    for i in range(max(len(arxiv_papers), len(scholar_papers))):
        if i < len(arxiv_papers):
            paper = arxiv_papers[i]
            if paper["hash"] not in papers_dict:
                papers_dict[paper["hash"]] = paper

        if i < len(scholar_papers):
            paper = scholar_papers[i]
            if paper["hash"] not in papers_dict:
                papers_dict[paper["hash"]] = paper

    # 转换回列表并排序
    papers = list(papers_dict.values())
    papers.sort(key=lambda x: str(x["published"]), reverse=True)

    return papers[:max_results]


def analyze_papers(papers: List[Dict]) -> str:
    """分析论文并生成报告，确保显示来源多样性"""
    if not papers:
        return "No relevant papers found in either arXiv or Google Scholar."

    # 按来源分类论文
    arxiv_papers = [p for p in papers if p["source"] == "arxiv"]
    scholar_papers = [p for p in papers if p["source"] == "scholar"]

    report = f"""Found {len(papers)} relevant papers:
- {len(arxiv_papers)} from arXiv
- {len(scholar_papers)} from Google Scholar

Detailed Analysis:\n\n"""

    for paper in papers:
        report += f"[{paper['source'].upper()}]\n"
        report += f"Title: {paper['title']}\n"
        report += f"Authors: {', '.join(paper['authors'])}\n"
        report += f"ID/URL: {paper['url']}\n"
        report += f"Published: {paper['published']}\n"
        report += f"Abstract: {paper['abstract']}\n\n"

    return report


def verify_paper(title: str) -> bool:
    """验证论文是否存在（在两个数据源中查找）"""
    try:
        # 尝试在 arXiv 中查找
        arxiv_results = _search_arxiv(title, max_results=1)
        if arxiv_results:
            return True

        # 尝试在 Scholar 中查找
        scholar_results = _search_scholarly(title, max_results=1)
        if scholar_results:
            return True

        return False
    except:
        return False


class ScientistUserAgent:
    def __init__(self):
        self.agent = ConversableAgent(
            name="User",
            llm_config=False,
            human_input_mode="NEVER",
        )

        self.agent.register_for_execution(name="search_and_analyze")(search_and_analyze)

    def get_agent(self):
        """获取配置了函数的智能体"""
        return self.agent
