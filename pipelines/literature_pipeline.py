from pipelines.base_pipeline import BasePipeline
from agents.retrieval_agent import RetrievalAgent
from agents.parsing_agent import ParsingAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.synthesis_agent import SynthesisAgent
from agents.insight_agent import InsightAgent
from agents.report_agent import ReportAgent
from agents.exploration_agent import ExplorationAgent
import logging

logger = logging.getLogger(__name__)


class LiteraturePipeline(BasePipeline):
    """Main literature research pipeline with error handling"""

    def run(self, plan):
        """Run complete literature research pipeline"""
        try:
            logger.info(f"Starting literature pipeline for topic: {getattr(plan, 'original_query', 'unknown')}")
            
            # Initialize agents
            retrieval = RetrievalAgent()
            explorer = ExplorationAgent(max_depth=2)
            parsing = ParsingAgent()
            knowledge = KnowledgeAgent()
            synthesis = SynthesisAgent()
            insight = InsightAgent()
            report = ReportAgent()
            
            # Step 1: Retrieve initial papers
            logger.info("Retrieving initial papers")
            papers = retrieval.run(plan)
            logger.info(f"Retrieved {len(papers)} initial papers")
            
            # Step 2: Explore related papers recursively
            logger.info("Exploring related papers")
            papers = explorer.explore(papers)
            logger.info(f"Expanded to {len(papers)} papers after exploration")
            
            # Step 3: Parse papers
            logger.info("Parsing paper content")
            parsed_papers = parsing.run(papers)
            logger.info(f"Successfully parsed {len(parsed_papers)} papers")
            
            # Step 4: Build knowledge graph
            logger.info("Building knowledge graph")
            knowledge_nodes = knowledge.run(parsed_papers)
            logger.info(f"Created {len(knowledge_nodes)} knowledge nodes")
            
            # Step 5: Synthesize findings
            logger.info("Synthesizing research findings")
            synthesis_results = synthesis.run(knowledge_nodes)
            
            # Step 6: Generate insights
            logger.info("Generating research insights")
            insights = insight.run(synthesis_results)
            
            # Step 7: Generate report
            logger.info("Generating final report")
            report_result = report.run(plan, papers, synthesis_results, insights)
            
            logger.info("Literature pipeline completed successfully")
            return report_result
            
        except Exception as e:
            logger.error(f"Error in LiteraturePipeline: {str(e)}")
            # Return error report instead of crashing
            return self._create_error_report(plan, str(e))
    
    def _create_error_report(self, plan, error_message):
        """Create a fallback error report"""
        logger.info("Creating error report")
        
        class ErrorReport:
            def __init__(self, query, error):
                self.query = query
                self.error = error
                self.summary = f"Research pipeline encountered an error: {error}"
                self.key_findings = ["Pipeline execution failed"]
                self.research_gaps = ["Unable to complete analysis due to error"]
                self.future_directions = ["Fix pipeline issues and retry"]
                self.paper_count = 0
                self.sources = []
        
        return ErrorReport(getattr(plan, 'original_query', 'unknown topic'), error_message)