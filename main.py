from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).with_name("fertilizer.csv")
YEAR_PREFIX = "Y"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the fertilizer CSV into a DataFrame."""
    return pd.read_csv(path)


def get_year_columns(df: pd.DataFrame) -> list[str]:
    """Return the wide-format year columns from the dataset."""
    return [column for column in df.columns if column.startswith(YEAR_PREFIX)]


def prepare_export_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only export rows and year-related columns for the first assignment step."""
    year_columns = get_year_columns(df)
    export_df = df.loc[df["Element"] == "Export quantity (tonnes N)", year_columns].copy()
    return export_df


def main() -> None:
    df = load_data()
    export_df = prepare_export_rows(df)

    print(f"Loaded rows: {len(df):,}")
    print(f"Prepared export rows: {len(export_df):,}")
    print(f"Year columns: {list(export_df.columns)}")
    print(export_df.head())


if __name__ == "__main__":
    main()
