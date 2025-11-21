import sys
import os
import pytest
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[1]

# src yolunu sys.path'e ekle
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# manuel olarak claim_ml modulunun yerini belirtiyoruz.


@pytest.fixture
def test_dataset_path():
    return Path(project_root) / "test" / "test_datasets"

@pytest.fixture
def empty_dataset(test_dataset_path):
    return pd.read_csv(test_dataset_path / "test_empty.csv")

@pytest.fixture
def load_csv_data(test_dataset_path):
    return pd.read_csv(test_dataset_path / "test.csv")


@pytest.fixture
def load_parquet_data(test_dataset_path):
    return pd.read_parquet(test_dataset_path / "test.parquet")
