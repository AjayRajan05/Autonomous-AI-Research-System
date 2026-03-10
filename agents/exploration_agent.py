import logging
from tools.arxiv_search import search_arxiv

logger = logging.getLogger(__name__)


class ExplorationAgent:

    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def explore(self, seed_papers):
        """Explore related papers recursively"""
        try:
            explored_titles = set()
            all_papers = list(seed_papers)  # Start with seed papers
            
            logger.info(f"Starting exploration with {len(seed_papers)} seed papers, max_depth={self.max_depth}")
            
            frontier = list(seed_papers)
            
            for depth in range(self.max_depth):
                logger.info(f"Exploration depth {depth + 1}/{self.max_depth}")
                
                new_frontier = []
                
                for paper in frontier:
                    try:
                        # Get paper title safely
                        title = getattr(paper, 'title', getattr(paper, 'title', 'unknown'))
                        
                        if title in explored_titles:
                            continue
                        
                        explored_titles.add(title)
                        
                        # Search for related papers using title as query
                        related_papers = search_arxiv(title)
                        
                        for related_paper in related_papers:
                            related_title = getattr(related_paper, 'title', getattr(related_paper, 'title', 'unknown'))
                            
                            if related_title not in explored_titles:
                                new_frontier.append(related_paper)
                        
                        logger.info(f"Found {len(related_papers)} related papers for: {title[:50]}...")
                        
                    except Exception as e:
                        logger.warning(f"Error exploring paper: {str(e)}")
                        continue
                
                frontier = new_frontier
                
                if not frontier:
                    logger.info(f"No new papers found at depth {depth + 1}, stopping exploration")
                    break
            
            # Combine all papers and remove duplicates
            final_papers = self._deduplicate_exploration(all_papers + frontier)
            
            logger.info(f"Exploration completed. Found {len(final_papers)} total papers")
            return final_papers
            
        except Exception as e:
            logger.error(f"Error in ExplorationAgent.explore: {str(e)}")
            return seed_papers  # Return original papers on error
    
    def _deduplicate_exploration(self, papers):
        """Remove duplicates from exploration results"""
        try:
            seen_titles = set()
            unique_papers = []
            
            for paper in papers:
                title = getattr(paper, 'title', getattr(paper, 'title', 'unknown'))
                
                if title not in seen_titles:
                    seen_titles.add(title)
                    unique_papers.append(paper)
            
            return unique_papers
            
        except Exception as e:
            logger.error(f"Error in exploration deduplication: {str(e)}")
            return papers[:50]  # Fallback limitation