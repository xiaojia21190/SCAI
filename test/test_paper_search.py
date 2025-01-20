# Test case
from agents.paper_metadata_finder import PaperMetaSearcher


def test_paper_searcher():
    searcher = PaperMetaSearcher(max_results=3)
    query = "Artificial Intelligence"
    result = searcher.search_and_analyze(query, "OPEN")
    assert "Found" in result, f"Test failed! Result: {result}"
    print(result)


# Run test
test_paper_searcher()
