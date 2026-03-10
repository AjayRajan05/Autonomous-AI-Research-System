"""
Run ML experiments on extracted models/datasets.
"""

import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.datasets import make_classification, load_iris, load_wine
import torch
import torch.nn as nn
import torch.optim as optim

logger = logging.getLogger(__name__)


class ExperimentAgent:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"ExperimentAgent initialized on device: {self.device}")

    def run(self, ml_components):
        """Run ML experiments based on extracted components"""
        results = []
        
        try:
            # Extract models and configurations
            models = ml_components.get("models", ["random_forest", "logistic_regression"])
            datasets = ml_components.get("datasets", ["synthetic"])
            hyperparams = ml_components.get("hyperparameters", {})
            
            logger.info(f"Running experiments for models: {models}")
            
            for model_name in models:
                for dataset_name in datasets:
                    logger.info(f"Testing {model_name} on {dataset_name}")
                    
                    # Load dataset
                    X, y = self._load_dataset(dataset_name)
                    
                    # Run experiment
                    result = self._run_experiment(model_name, X, y, hyperparams)
                    result["model"] = model_name
                    result["dataset"] = dataset_name
                    
                    results.append(result)
                    logger.info(f"Experiment completed: {model_name} on {dataset_name} - Accuracy: {result['accuracy']:.3f}")
            
            logger.info(f"Total experiments completed: {len(results)}")
            return results
            
        except Exception as e:
            logger.error(f"Error in ExperimentAgent.run: {str(e)}")
            return [{"model": "error", "dataset": "error", "accuracy": 0.0, "error": str(e)}]

    def _load_dataset(self, dataset_name):
        """Load dataset for experimentation"""
        try:
            if dataset_name == "synthetic":
                X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
            elif dataset_name == "iris":
                data = load_iris()
                X, y = data.data, data.target
            elif dataset_name == "wine":
                data = load_wine()
                X, y = data.data, data.target
            else:
                # Default to synthetic
                X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading dataset {dataset_name}: {str(e)}")
            # Fallback to synthetic data
            return make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)

    def _run_experiment(self, model_name, X, y, hyperparams):
        """Run a single ML experiment"""
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            result = {"model": model_name, "accuracy": 0.0, "f1_score": 0.0}
            
            if model_name == "random_forest":
                result = self._run_random_forest(X_train, X_test, y_train, y_test, hyperparams)
            elif model_name == "logistic_regression":
                result = self._run_logistic_regression(X_train, X_test, y_train, y_test, hyperparams)
            elif model_name == "neural_network":
                result = self._run_neural_network(X_train, X_test, y_train, y_test, hyperparams)
            elif model_name == "transformer":
                result = self._run_simple_transformer(X_train, X_test, y_train, y_test, hyperparams)
            else:
                # Default to random forest
                result = self._run_random_forest(X_train, X_test, y_train, y_test, hyperparams)
            
            return result
            
        except Exception as e:
            logger.error(f"Error running experiment for {model_name}: {str(e)}")
            return {"model": model_name, "accuracy": 0.0, "f1_score": 0.0, "error": str(e)}

    def _run_random_forest(self, X_train, X_test, y_train, y_test, hyperparams):
        """Run Random Forest experiment"""
        n_estimators = hyperparams.get("n_estimators", 100)
        max_depth = hyperparams.get("max_depth", 10)
        
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        return {
            "model": "random_forest",
            "accuracy": accuracy,
            "f1_score": f1,
            "n_estimators": n_estimators,
            "max_depth": max_depth
        }

    def _run_logistic_regression(self, X_train, X_test, y_train, y_test, hyperparams):
        """Run Logistic Regression experiment"""
        C = hyperparams.get("C", 1.0)
        
        model = LogisticRegression(C=C, random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        return {
            "model": "logistic_regression",
            "accuracy": accuracy,
            "f1_score": f1,
            "C": C
        }

    def _run_neural_network(self, X_train, X_test, y_train, y_test, hyperparams):
        """Run simple Neural Network experiment"""
        input_dim = X_train.shape[1]
        hidden_dim = hyperparams.get("hidden_dim", 64)
        learning_rate = hyperparams.get("lr", 0.001)
        epochs = hyperparams.get("epochs", 100)
        
        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device)
        
        # Simple neural network
        model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, len(np.unique(y_train)))
        ).to(self.device)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
        
        # Evaluation
        model.eval()
        with torch.no_grad():
            outputs = model(X_test_tensor)
            _, predicted = torch.max(outputs.data, 1)
            
            y_pred_cpu = predicted.cpu().numpy()
            accuracy = accuracy_score(y_test, y_pred_cpu)
            f1 = f1_score(y_test, y_pred_cpu, average='weighted')
        
        return {
            "model": "neural_network",
            "accuracy": accuracy,
            "f1_score": f1,
            "hidden_dim": hidden_dim,
            "epochs": epochs,
            "learning_rate": learning_rate
        }

    def _run_simple_transformer(self, X_train, X_test, y_train, y_test, hyperparams):
        """Run a simplified transformer-like model (using attention mechanism)"""
        # For tabular data, we'll use a simple attention mechanism
        # This is a simplified version since full transformers are for sequential data
        
        input_dim = X_train.shape[1]
        embed_dim = hyperparams.get("embed_dim", 64)
        learning_rate = hyperparams.get("lr", 0.001)
        epochs = hyperparams.get("epochs", 50)
        
        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device)
        
        # Simple attention-based model
        class SimpleAttention(nn.Module):
            def __init__(self, input_dim, embed_dim, num_classes):
                super().__init__()
                self.query = nn.Linear(input_dim, embed_dim)
                self.key = nn.Linear(input_dim, embed_dim)
                self.value = nn.Linear(input_dim, embed_dim)
                self.classifier = nn.Linear(embed_dim, num_classes)
                
            def forward(self, x):
                Q = self.query(x)
                K = self.key(x)
                V = self.value(x)
                
                # Simple attention
                attention = torch.softmax(Q * K / (embed_dim ** 0.5), dim=-1)
                attended = attention * V
                
                return self.classifier(attended)
        
        model = SimpleAttention(input_dim, embed_dim, len(np.unique(y_train))).to(self.device)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
        
        # Evaluation
        model.eval()
        with torch.no_grad():
            outputs = model(X_test_tensor)
            _, predicted = torch.max(outputs.data, 1)
            
            y_pred_cpu = predicted.cpu().numpy()
            accuracy = accuracy_score(y_test, y_pred_cpu)
            f1 = f1_score(y_test, y_pred_cpu, average='weighted')
        
        return {
            "model": "transformer",
            "accuracy": accuracy,
            "f1_score": f1,
            "embed_dim": embed_dim,
            "epochs": epochs,
            "learning_rate": learning_rate
        }