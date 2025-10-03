"""Exploratory Data Analysis for multi-table datasets."""

from typing import Any

import pandas as pd


def analyze_dataset(data: dict[str, pd.DataFrame], metadata: dict[str, Any] | Any) -> dict[str, Any]:
    """
    Perform exploratory data analysis on a multi-table dataset.

    Args:
        data: Dictionary mapping table names to DataFrames
        metadata: SDV metadata dictionary or Metadata object

    Returns:
        Dictionary containing analysis results
    """
    # Convert Metadata object to dict if needed
    if hasattr(metadata, 'to_dict'):
        metadata = metadata.to_dict()

    analysis = {
        'summary': {},
        'table_stats': {},
        'relationships': metadata.get('relationships', [])
    }

    # Overall summary
    analysis['summary'] = {
        'num_tables': len(data),
        'total_rows': sum(df.shape[0] for df in data.values()),
        'total_columns': sum(df.shape[1] for df in data.values()),
    }

    # Per-table statistics
    for table_name, df in data.items():
        table_meta = metadata['tables'].get(table_name, {})
        pk = table_meta.get('primary_key', '')

        analysis['table_stats'][table_name] = {
            'shape': df.shape,
            'primary_key': pk,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict(),
        }

    return analysis


def print_dataset_summary(data: dict[str, pd.DataFrame], metadata: dict[str, Any] | Any) -> None:
    """Print a formatted summary of the dataset."""
    analysis = analyze_dataset(data, metadata)

    print("=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)
    print(f"Tables: {analysis['summary']['num_tables']}")
    print(f"Total Rows: {analysis['summary']['total_rows']:,}")
    print(f"Total Columns: {analysis['summary']['total_columns']}")
    print()

    print("=" * 80)
    print("TABLE DETAILS")
    print("=" * 80)
    for table_name, stats in analysis['table_stats'].items():
        print(f"\n{table_name}")
        print("-" * 80)
        print(f"  Shape: {stats['shape']}")
        print(f"  Primary Key: {stats['primary_key']}")
        print(f"  Memory: {stats['memory_usage_mb']:.2f} MB")
        print(f"  Missing Values: {sum(stats['missing_values'].values())}")
        if sum(stats['missing_values'].values()) > 0:
            missing = {k: v for k, v in stats['missing_values'].items() if v > 0}
            print(f"    {missing}")

    print()
    print("=" * 80)
    print("RELATIONSHIPS")
    print("=" * 80)
    for rel in analysis['relationships']:
        print(f"  {rel['parent_table_name']}.{rel['parent_primary_key']} "
              f"→ {rel['child_table_name']}.{rel['child_foreign_key']}")


def get_table_preview(data: dict[str, pd.DataFrame], table_name: str, n: int = 5) -> pd.DataFrame:
    """Get first n rows of a table."""
    return data[table_name].head(n)


def get_column_stats(df: pd.DataFrame, column: str) -> dict[str, Any]:
    """Get detailed statistics for a specific column."""
    col_data = df[column]
    stats = {
        'dtype': str(col_data.dtype),
        'missing': col_data.isnull().sum(),
        'missing_pct': (col_data.isnull().sum() / len(col_data)) * 100,
        'unique': col_data.nunique(),
    }

    if pd.api.types.is_numeric_dtype(col_data):
        stats.update({
            'min': col_data.min(),
            'max': col_data.max(),
            'mean': col_data.mean(),
            'median': col_data.median(),
            'std': col_data.std(),
        })
    elif pd.api.types.is_categorical_dtype(col_data) or pd.api.types.is_object_dtype(col_data):
        stats['top_values'] = col_data.value_counts().head(10).to_dict()

    return stats


def explore_table(data: dict[str, pd.DataFrame], table_name: str) -> None:
    """Print detailed exploration of a specific table."""
    df = data[table_name]

    print(f"{'=' * 80}")
    print(f"TABLE: {table_name}")
    print(f"{'=' * 80}")
    print(f"Shape: {df.shape}")
    print(f"\nColumn Types:")
    print(df.dtypes)
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nBasic Statistics:")
    print(df.describe(include='all'))
