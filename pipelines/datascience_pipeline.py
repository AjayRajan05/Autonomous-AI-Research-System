from pipelines.literature_pipeline import LiteraturePipeline
from agents.experimental.experiment_agent import ExperimentAgent
from agents.experimental.evaluation_agent import EvaluationAgent
import logging

logger = logging.getLogger(__name__)


class DatasciencePipeline(LiteraturePipeline):
    """Extended pipeline for data science research with ML experiments"""
    
    def run(self, plan):
        """Run full research pipeline with ML experiments"""
        try:
            # Run literature pipeline first
            logger.info("Starting literature review phase")
            literature_report = super().run(plan)
            
            # Extract ML models and datasets from papers
            logger.info("Extracting ML models and datasets")
            ml_components = self._extract_ml_components(literature_report)
            
            # Run ML experiments
            logger.info("Running ML experiments")
            experiment_agent = ExperimentAgent()
            experiment_results = experiment_agent.run(ml_components)
            
            # Evaluate experiments
            logger.info("Evaluating experiment results")
            evaluation_agent = EvaluationAgent()
            evaluation_results = evaluation_agent.run(experiment_results, ml_components)
            
            # Enhance report with experiment results
            enhanced_report = self._enhance_report_with_experiments(
                literature_report, experiment_results, evaluation_results
            )
            
            logger.info("Data science pipeline completed successfully")
            return enhanced_report
            
        except Exception as e:
            logger.error(f"Error in DatasciencePipeline: {str(e)}")
            raise
    
    def _extract_ml_components(self, literature_report):
        """Extract ML models, datasets, and methodologies from papers"""
        # This would parse papers to extract:
        # - Model architectures
        # - Datasets used
        # - Hyperparameters
        # - Evaluation metrics
        
        # For now, return placeholder structure
        return {
            "models": ["transformer", "cnn", "rnn"],
            "datasets": ["imagenet", "cifar10", "custom"],
            "hyperparameters": {"lr": [0.001, 0.01], "batch_size": [32, 64]},
            "metrics": ["accuracy", "f1_score", "precision"]
        }
    
    def _enhance_report_with_experiments(self, literature_report, experiment_results, evaluation_results):
        """Add experiment results to the literature report"""
        # This would merge the experiment results into the original report
        enhanced_report = literature_report.copy() if hasattr(literature_report, 'copy') else literature_report
        
        # Add experiment section
        experiment_section = {
            "experiments_performed": len(experiment_results),
            "experiment_results": experiment_results,
            "model_performance": evaluation_results,
            "best_model": max(evaluation_results.keys(), key=lambda k: evaluation_results[k]) if evaluation_results else None
        }
        
        if hasattr(enhanced_report, '__dict__'):
            enhanced_report.experiments = experiment_section
        else:
            enhanced_report['experiments'] = experiment_section
            
        return enhanced_report