from pipelines.base_pipeline import BasePipeline
from agents.retrieval_agent import RetrievalAgent
from agents.parsing_agent import ParsingAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.synthesis_agent import SynthesisAgent
from agents.insight_agent import InsightAgent
from agents.report_agent import ReportAgent
from agents.exploration_agent import ExplorationAgent


class LiteraturePipeline(BasePipeline):

    def run(self, plan):
        explorer = ExplorationAgent(max_depth=2)
        retrieval = RetrievalAgent()
        parsing = ParsingAgent()
        knowledge = KnowledgeAgent()
        synthesis = SynthesisAgent()
        insight = InsightAgent()
        report = ReportAgent()

        papers = self.retriever.retrieve(topic)

        # NEW: recursive exploration
        papers = self.explorer.explore(papers)

        parsed = self.parser.parse(papers)

        knowledge = self.knowledge.build(parsed)
#########################
        #papers = retrieval.run(plan)

        #papers = parsing.run(papers)

        nodes = knowledge.run(papers)

        syn = synthesis.run(nodes)

        ins = insight.run(syn)

        return report.run(plan, papers, syn, ins)