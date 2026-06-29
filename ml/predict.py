"""Spam prediction module."""

import os
import joblib
import numpy as np
from pathlib import Path

from ml.preprocess import prepare_email_text


class SpamPredictor:
    """Spam detection predictor using pre-trained model."""
    
    def __init__(self, model_path: str = "model.pkl", vectorizer_path: str = "vectorizer.pkl"):
        self.model = None
        self.vectorizer = None
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the pre-trained model and vectorizer."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}. "
                "Please ensure model.pkl is in the project root."
            )
        
        if not self.vectorizer_path.exists():
            raise FileNotFoundError(
                f"Vectorizer file not found: {self.vectorizer_path}. "
                "Please ensure vectorizer.pkl is in the project root."
            )
        
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
    
    def predict(self, subject: str, body: str) -> dict:
        """
        Predict if email is spam or ham.
        
        Returns dict with:
            - prediction: "Spam" or "Ham"
            - probability: float (spam probability)
            - confidence: float (confidence in prediction)
        """
        # Preprocess text
        processed_text = prepare_email_text(subject, body)
        
        if not processed_text:
            # Empty text defaults to ham with low confidence
            return {
                "prediction": "Ham",
                "probability": 0.0,
                "confidence": 0.5,
            }
        
        # Vectorize
        text_vectorized = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(text_vectorized)[0]
        
        # Get probability if available
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(text_vectorized)[0]
            # Assuming class 1 is spam
            spam_prob = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            confidence = max(probabilities)
        else:
            spam_prob = 1.0 if prediction == 1 else 0.0
            confidence = 1.0
        
        return {
            "prediction": "Spam" if prediction == 1 else "Ham",
            "probability": float(spam_prob),
            "confidence": float(confidence),
        }
    
    def predict_batch(self, emails: list[dict]) -> list[dict]:
        """
        Predict spam/ham for a batch of emails.
        
        Adds prediction data to each email dict.
        """
        results = []
        
        for email in emails:
            prediction = self.predict(email.get("subject", ""), email.get("body", ""))
            email_result = {**email, **prediction}
            results.append(email_result)
        
        return results
