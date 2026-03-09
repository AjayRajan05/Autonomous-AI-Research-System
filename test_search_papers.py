from tools.arxiv_tool import search_arxiv

papers = search_arxiv("graph neural networks traffic prediction")

for p in papers:
    print(p["title"])