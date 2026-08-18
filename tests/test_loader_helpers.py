import pandas as pd
import pytest

from scripts.load_demo_data import validate_required_columns


def test_validate_required_columns_accepts_expected_schema() -> None:
    df = pd.DataFrame({"a": [1], "b": [2]})
    validate_required_columns(df, {"a", "b"}, "test.csv")


def test_validate_required_columns_rejects_missing_schema() -> None:
    df = pd.DataFrame({"a": [1]})

    with pytest.raises(ValueError, match="faltan columnas obligatorias"):
        validate_required_columns(df, {"a", "b"}, "test.csv")
