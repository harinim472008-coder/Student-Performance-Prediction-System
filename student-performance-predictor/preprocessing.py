from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd


FEATURE_COLUMNS: List[str] = ["attendance", "study_hours", "previous_grades"]
TARGET_COLUMN = "final_score"


@dataclass
class StandardScaler:
    mean_: np.ndarray
    std_: np.ndarray

    def transform(self, x: np.ndarray) -> np.ndarray:
        safe_std = np.where(self.std_ == 0, 1.0, self.std_)
        return (x - self.mean_) / safe_std


def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data = data.drop_duplicates()
    data[FEATURE_COLUMNS + [TARGET_COLUMN]] = data[
        FEATURE_COLUMNS + [TARGET_COLUMN]
    ].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    return data


def split_features_target(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    x = df[FEATURE_COLUMNS].to_numpy(dtype=float)
    y = df[TARGET_COLUMN].to_numpy(dtype=float)
    return x, y


def fit_standard_scaler(x: np.ndarray) -> StandardScaler:
    return StandardScaler(mean_=x.mean(axis=0), std_=x.std(axis=0))

