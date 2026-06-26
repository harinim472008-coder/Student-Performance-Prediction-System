from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd

from preprocessing import FEATURE_COLUMNS, fit_standard_scaler


@dataclass
class StudentPerformanceModel:
    weights_: np.ndarray | None = None
    scaler_: object | None = None
    r2_score_: float | None = None
    rmse_: float | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.scaler_ = fit_standard_scaler(x)
        x_scaled = self.scaler_.transform(x)
        x_bias = np.c_[np.ones(x_scaled.shape[0]), x_scaled]

        # Use pseudo-inverse for numerical stability.
        self.weights_ = np.linalg.pinv(x_bias.T @ x_bias) @ x_bias.T @ y

        y_pred = x_bias @ self.weights_
        residuals = y - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        self.r2_score_ = float(1 - (ss_res / ss_tot if ss_tot != 0 else 0.0))
        self.rmse_ = float(np.sqrt(np.mean(residuals**2)))

    def predict_score(self, attendance: float, study_hours: float, previous_grades: float) -> float:
        if self.weights_ is None or self.scaler_ is None:
            raise RuntimeError("Model must be trained before prediction.")

        x = np.array([[attendance, study_hours, previous_grades]], dtype=float)
        x_scaled = self.scaler_.transform(x)
        x_bias = np.c_[np.ones(x_scaled.shape[0]), x_scaled]
        prediction = float((x_bias @ self.weights_)[0])
        return max(0.0, min(100.0, prediction))

    @staticmethod
    def performance_band(score: float) -> str:
        if score >= 85:
            return "Excellent"
        if score >= 70:
            return "Good"
        if score >= 55:
            return "Average"
        return "Needs Improvement"

    def stats_summary(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        return {
            col: {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std(ddof=0)),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
            }
            for col in FEATURE_COLUMNS + ["final_score"]
        }

