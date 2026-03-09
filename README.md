User Query
   ↓
Planner Agent
   ↓
Research Agent  → find papers
   ↓
Knowledge Memory (Vector DB)
   ↓
Experiment Agent → run ML code
   ↓
Evaluation Agent → compare results
   ↓
Report Agent → generate research report






                User Query
                     │
                     ▼
               Planner Agent
                     │
        ┌────────────┼─────────────┐
        ▼            ▼             ▼
Research Agent   Experiment Agent   Evaluation Agent
        │            │             │
        └────────────┼─────────────┘
                     ▼
                Memory (Vector DB)
                     ▼
                Report Agent
                     ▼
             Final Research Paper


autonomous-research-intelligence/
│
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py           # Decomposes query → subtopics + route decision
│   ├── retrieval_agent.py         # Searches arXiv, Semantic Scholar, PubMed
│   ├── parsing_agent.py           # Extracts sections from PDFs (PyMuPDF / GROBID)
│   ├── knowledge_agent.py         # Extracts claims, datasets, models, limitations
│   ├── synthesis_agent.py         # Compares papers, finds trends & contradictions
│   ├── insight_agent.py           # Detects gaps, open questions, future directions
│   ├── report_agent.py            # Generates final .md and .pdf report
│   │
│   └── experimental/              # Only used for Data Science route
│       ├── experiment_agent.py    # Designs + runs ML experiments
│       └── evaluation_agent.py    # Evaluates results vs. literature baselines
│
├── tools/
│   ├── __init__.py
│   ├── arxiv_search.py            # arXiv API wrapper
│   ├── semantic_scholar.py        # Semantic Scholar API wrapper
│   ├── pubmed_search.py           # PubMed API wrapper
│   ├── pdf_parser.py              # PyMuPDF-based PDF extraction
│   ├── web_search.py              # Fallback web search (Serper / Tavily)
│   └── knowledge_graph.py        # Builds + queries the research knowledge graph
│
├── memory/
│   ├── __init__.py
│   ├── vector_store.py            # ChromaDB / Qdrant embedding store
│   ├── paper_store.py             # Structured metadata store (SQLite)
│   └── session_memory.py         # Cross-agent shared state within a run
│
├── pipelines/
│   ├── __init__.py
│   ├── router.py                  # Intent analyzer: routes query to correct pipeline
│   ├── literature_pipeline.py     # Full literature research flow
│   ├── datascience_pipeline.py    # Literature + experiment flow
│   └── base_pipeline.py          # Shared pipeline base class
│
├── schemas/
│   ├── paper.py                   # Pydantic model for a parsed paper
│   ├── research_plan.py          # Pydantic model for planner output
│   ├── knowledge_node.py         # Pydantic model for extracted knowledge
│   └── report.py                 # Pydantic model for final report
│
├── reports/                       # Generated reports saved here
│   └── .gitkeep
│
├── cache/                         # Cached PDFs and API responses
│   └── .gitkeep
│
├── configs/
│   ├── settings.yaml              # API keys, model config, search limits
│   └── prompts.yaml              # All agent system prompts (editable)
│
├── tests/
│   ├── test_retrieval.py
│   ├── test_parsing.py
│   ├── test_pipeline.py
│   └── fixtures/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── main.py                        # CLI entrypoint
├── requirements.txt
└── README.md