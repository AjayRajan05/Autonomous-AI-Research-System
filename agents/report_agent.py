import markdown2
from pathlib import Path
from datetime import datetime
from slugify import slugify
from tools.pdf_report import markdown_to_pdf
from schemas.report import ResearchReport
from tools.config_loader import load_settings


settings = load_settings()


class ReportAgent:

    def run(self, plan, papers, synthesis, insights):

        summary = synthesis["consensus"]

        report = ResearchReport(
            query=plan.original_query,
            summary=summary,
            technologies=[],
            key_findings=synthesis["trends"],
            research_gaps=insights["gaps"],
            future_directions=insights["future_directions"],
            paper_count=len(papers),
            sources=[p.url for p in papers]
        )

        md = self.render_md(report)

        name = slugify(plan.original_query)

        ts = datetime.now().strftime("%Y%m%d_%H%M")

        path = Path(settings["paths"]["reports_dir"]) / f"{name}_{ts}.md"

        path.write_text(md)

        return report, path

    def render_md(self, report):

        md = f"""
        # Research Report

        Query: {report.query}

        ## Summary
        {report.summary}

        ## Key Findings
        {chr(10).join("- "+x for x in report.key_findings)}

        ## Research Gaps
        {chr(10).join("- "+x for x in report.research_gaps)}

        ## Future Directions
        {chr(10).join("- "+x for x in report.future_directions)}
        """

        return md

    def save_report(self, report):

        md_file = f"reports/{report.title}.md"
        pdf_file = f"reports/{report.title}.pdf"

        with open(md_file, "w") as f:
            f.write(report.content)

        markdown_to_pdf(report.content, pdf_file)

        return md_file, pdf_file