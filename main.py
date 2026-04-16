from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).with_name("fertilizer.csv")
OUTPUT_DIR = Path(__file__).parent
YEAR_PREFIX = "Y"
PERSIAN_GULF_COUNTRIES = [
    "Saudi Arabia",
    "Bahrain",
    "Iran",
    "Iraq",
    "Oman",
    "Qatar",
    "Kuwait",
    "United Arab Emirates",
]


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the fertilizer CSV into a DataFrame."""
    return pd.read_csv(path)


def get_year_columns(df: pd.DataFrame) -> list[str]:
    """Return the wide-format year columns from the dataset."""
    return [column for column in df.columns if column.startswith(YEAR_PREFIX)]


def prepare_export_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only nitrogen export rows from the assignment dataset."""
    return df.loc[df["Element"] == "Export quantity (tonnes N)"].copy()


def prepare_import_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only nitrogen import rows from the assignment dataset."""
    return df.loc[df["Element"] == "Import quantity (tonnes N)"].copy()


def reshape_years_long(df: pd.DataFrame) -> pd.DataFrame:
    """Convert wide Y1990...Y2023 columns into year/value rows."""
    year_columns = get_year_columns(df)
    id_columns = [column for column in df.columns if column not in year_columns]

    long_df = df.melt(
        id_vars=id_columns,
        value_vars=year_columns,
        var_name="year",
        value_name="value",
    )
    long_df["year"] = long_df["year"].str.removeprefix(YEAR_PREFIX).astype(int)
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df = long_df.dropna(subset=["value"])
    return long_df


def gulf_exports_over_time(long_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Persian Gulf nitrogen exports by country and year."""
    gulf_df = long_df.loc[
        long_df["Reporter Countries"].isin(PERSIAN_GULF_COUNTRIES)
    ].copy()
    grouped = (
        gulf_df.groupby(["year", "Reporter Countries"], as_index=False)["value"]
        .sum()
    )
    return grouped


def plot_gulf_exports_over_time(exports_df: pd.DataFrame) -> Path:
    """Create the stacked bar chart of Persian Gulf exports over time."""
    chart_df = (
        exports_df.pivot(index="year", columns="Reporter Countries", values="value")
        .fillna(0)
        .sort_index()
    )
    chart_df = chart_df.reindex(columns=PERSIAN_GULF_COUNTRIES, fill_value=0)

    ax = chart_df.plot(kind="bar", stacked=True, figsize=(14, 7), width=0.85)
    ax.set_title("Persian Gulf Nitrogen Fertilizer Exports Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Export Quantity (tonnes N)")
    ax.legend(title="Country", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "persian_gulf_exports_over_time.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def gulf_urea_share_of_global_exports(long_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Persian Gulf urea exports as a share of global nitrogen exports."""
    gulf_urea = (
        long_df.loc[
            long_df["Reporter Countries"].isin(PERSIAN_GULF_COUNTRIES)
            & (long_df["Item"] == "Urea")
        ]
        .groupby("year", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "gulf_urea_exports"})
    )

    global_exports = (
        long_df.groupby("year", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "global_exports"})
    )

    share_df = gulf_urea.merge(global_exports, on="year", how="inner")
    share_df["share_pct"] = (
        share_df["gulf_urea_exports"] / share_df["global_exports"] * 100
    )
    return share_df


def plot_gulf_urea_share_of_global_exports(share_df: pd.DataFrame) -> Path:
    """Create the line chart for Gulf urea export share."""
    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax1.plot(
        share_df["year"],
        share_df["gulf_urea_exports"],
        color="tab:blue",
        linewidth=2,
        label="Persian Gulf urea exports",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Urea Export Quantity (tonnes N)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(
        share_df["year"],
        share_df["share_pct"],
        color="tab:red",
        linewidth=2,
        linestyle="--",
        label="Share of global exports",
    )
    ax2.set_ylabel("Share of Global Exports (%)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    fig.suptitle("Persian Gulf Urea Exports and Share of Global Nitrogen Exports")
    fig.tight_layout()

    output_path = OUTPUT_DIR / "persian_gulf_urea_share_of_global_exports.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def top_importers_2023(import_df: pd.DataFrame) -> pd.DataFrame:
    """Return the top 10 nitrogen importers from Persian Gulf countries in 2023."""
    gulf_imports_2023 = import_df.loc[
        import_df["Partner Countries"].isin(PERSIAN_GULF_COUNTRIES)
    ].copy()
    gulf_imports_2023["Y2023"] = pd.to_numeric(
        gulf_imports_2023["Y2023"], errors="coerce"
    )
    gulf_imports_2023 = gulf_imports_2023.dropna(subset=["Y2023"])

    top_10 = (
        gulf_imports_2023.groupby("Reporter Countries", as_index=False)["Y2023"]
        .sum()
        .sort_values("Y2023", ascending=False)
        .head(10)
        .rename(columns={"Reporter Countries": "Importer", "Y2023": "2023 Imports (t)"})
    )
    return top_10


def main() -> None:
    df = load_data()

    export_df = prepare_export_rows(df)
    long_df = reshape_years_long(export_df)

    gulf_exports_df = gulf_exports_over_time(long_df)
    share_df = gulf_urea_share_of_global_exports(long_df)

    import_df = prepare_import_rows(df)
    top_importers_df = top_importers_2023(import_df)

    chart_one = plot_gulf_exports_over_time(gulf_exports_df)
    chart_two = plot_gulf_urea_share_of_global_exports(share_df)

    print(f"Loaded rows: {len(df):,}")
    print(f"Nitrogen export rows: {len(export_df):,}")
    print(f"Nitrogen import rows: {len(import_df):,}")
    print(f"Long-format rows: {len(long_df):,}")
    print(f"Saved: {chart_one.name}")
    print(f"Saved: {chart_two.name}")
    print("\nTop 10 importers in 2023 from Persian Gulf countries:")
    print(top_importers_df.to_string(index=False))


if __name__ == "__main__":
    main()
