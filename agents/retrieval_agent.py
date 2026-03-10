import logging
from tools.arxiv_search import search as arxiv_search
from tools.semantic_scholar import search as ss_search
from rapidfuzz import fuzz
from schemas.paper import Paper

logger = logging.getLogger(__name__)


class RetrievalAgent:

    def run(self, plan):
        """Retrieve papers from multiple sources"""
        try:
            papers = []
            
            # Get search queries from plan
            search_queries = getattr(plan, 'search_queries', [getattr(plan, 'original_query', 'research')])
            max_papers = getattr(plan, 'max_papers', 20)
            
            logger.info(f"Retrieving papers for queries: {search_queries}")
            
            for query in search_queries:
                try:
                    # Search from multiple sources
                    arxiv_papers = arxiv_search(query, 5)
                    ss_papers = ss_search(query, 5)
                    
                    papers.extend(arxiv_papers)
                    papers.extend(ss_papers)
                    
                    logger.info(f"Found {len(arxiv_papers)} arXiv papers and {len(ss_papers)} Semantic Scholar papers for query: {query}")
                    
                except Exception as e:
                    logger.warning(f"Error searching for query '{query}': {str(e)}")
                    continue
            
            # Remove duplicates
            unique_papers = self._deduplicate_papers(papers)
            
            # Limit results
            final_papers = unique_papers[:max_papers]
            
            logger.info(f"Retrieved {len(final_papers)} unique papers after deduplication")
            return final_papers
            
        except Exception as e:
            logger.error(f"Error in RetrievalAgent.run: {str(e)}")
            return []
    
    def _deduplicate_papers(self, papers):
        """Remove duplicate papers based on title similarity"""
        try:
            unique_papers = {}
            
            for paper in papers:
                if not hasattr(paper, 'title') or not paper.title:
                    continue
                    
                title_lower = paper.title.lower()
                
                # Check for similar titles
                is_duplicate = False
                for existing_title in unique_papers.keys():
                    similarity = fuzz.ratio(title_lower, existing_title)
                    if similarity > 90:  # High similarity threshold
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_papers[title_lower] = paper
            
            return list(unique_papers.values())
            
        except Exception as e:
            logger.error(f"Error in deduplication: {str(e)}")
            return papers[:10]  # Fallback to first 10 papers