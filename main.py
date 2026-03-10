import argparse
import logging
import sys
from pathlib import Path
from pipelines.router import Router
from memory.session_memory import SessionMemory
from tools.config_loader import load_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('research_platform.log')
    ]
)

logger = logging.getLogger(__name__)


def interactive_mode():
    """Interactive mode for user input"""
    print("=" * 60)
    print(" AI Research Platform - Interactive Mode")
    print("=" * 60)
    print("\nAvailable modes:")
    print("1. literature - Literature review and synthesis")
    print("2. datascience - Literature review + ML experiments")
    print("\n")
    
    while True:
        try:
            # Get research topic
            topic = input(" Enter your research topic (or 'quit' to exit): ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print(" Goodbye!")
                break
            
            if not topic:
                print(" Please enter a valid research topic.")
                continue
            
            # Get mode
            mode_input = input(" Select mode [literature/datascience] (default: literature): ").strip()
            mode = mode_input.lower() if mode_input else 'literature'
            
            if mode not in ['literature', 'datascience']:
                print(" Invalid mode. Using 'literature' as default.")
                mode = 'literature'
            
            print(f"\n Starting research on: '{topic}' using {mode} mode...")
            print("-" * 60)
            
            # Run research
            success = run_research(topic, mode)
            
            if success:
                print(f"\n Research completed successfully!")
                print(f" Reports saved in: {load_settings()['paths']['reports_dir']}")
            else:
                print(f"\n Research encountered errors. Check logs for details.")
            
            print("\n" + "=" * 60)
            
        except KeyboardInterrupt:
            print("\n Research interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f" An error occurred: {str(e)}")


def run_research(topic, mode):
    """Run research pipeline with proper error handling"""
    try:
        # Initialize components
        memory = SessionMemory()
        router = Router(memory)
        
        # Get pipeline
        pipeline = router.route(mode)
        
        # Create research plan
        from agents.planner_agent import PlannerAgent
        planner = PlannerAgent()
        plan = planner.run(topic)
        
        # Run pipeline
        report = pipeline.run(plan)
        
        # Generate PDF report if available
        if hasattr(report, '__dict__') and hasattr(report, 'query'):
            generate_pdf_report(report)
        
        return True
        
    except Exception as e:
        logger.error(f"Error running research: {str(e)}")
        return False


def generate_pdf_report(report):
    """Generate PDF report from research results"""
    try:
        from tools.pdf_report import markdown_to_pdf
        from slugify import slugify
        from datetime import datetime
        import markdown2
        
        # Create markdown content
        md_content = f"""
# Research Report

**Topic:** {report.query}

## Summary
{getattr(report, 'summary', 'No summary available')}

## Key Findings
{chr(10).join(f"- {finding}" for finding in getattr(report, 'key_findings', []))}

## Research Gaps
{chr(10).join(f"- {gap}" for gap in getattr(report, 'research_gaps', []))}

## Future Directions
{chr(10).join(f"- {direction}" for direction in getattr(report, 'future_directions', []))}

## Sources
{chr(10).join(f"- {source}" for source in getattr(report, 'sources', []))}
"""
        
        # Save files
        settings = load_settings()
        reports_dir = Path(settings["paths"]["reports_dir"])
        reports_dir.mkdir(exist_ok=True)
        
        # Generate filename
        topic_slug = slugify(report.query)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save markdown
        md_file = reports_dir / f"{topic_slug}_{timestamp}.md"
        md_file.write_text(md_content, encoding='utf-8')
        
        # Save PDF
        pdf_file = reports_dir / f"{topic_slug}_{timestamp}.pdf"
        markdown_to_pdf(md_content, str(pdf_file))
        
        logger.info(f"Reports saved: {md_file} and {pdf_file}")
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Research Platform - Autonomous research automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Graph Neural Networks for Drug Discovery"
  python main.py --topic "AI agents for autonomous software development" --mode datascience
  python main.py --interactive  # For interactive mode
        """
    )
    
    parser.add_argument("--topic", type=str, help="Research topic")
    parser.add_argument("--mode", type=str, default="literature", 
                       choices=["literature", "datascience"],
                       help="Research mode: literature or datascience")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    try:
        if args.interactive or not args.topic:
            # Interactive mode
            interactive_mode()
        else:
            # Command line mode
            logger.info(f"Starting research on topic: {args.topic}")
            logger.info(f"Using mode: {args.mode}")
            
            success = run_research(args.topic, args.mode)
            
            if success:
                print("\n Research completed successfully!")
                print(f" Reports saved in: {load_settings()['paths']['reports_dir']}")
            else:
                print("\n Research failed. Check logs for details.")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n Research interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f" Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()