"""Test script for ERD and EDA modules."""

from sdv.datasets.demo import download_demo

from allianz_dbt_assignment.erd import generate_erd
from allianz_dbt_assignment.eda import print_dataset_summary, explore_table


def test_erd():
    """Test ERD generation."""
    print("=" * 80)
    print("Testing ERD Generation")
    print("=" * 80)

    # Load sample data
    data, metadata = download_demo(
        modality='multi_table',
        dataset_name='financial_v1'
    )

    print(f"Loaded dataset with {len(data)} tables")
    print(f"Tables: {list(data.keys())}")
    print()

    # Test ERD generation
    try:
        erd = generate_erd(metadata, output_path='dev/financial_erd')
        print("✓ ERD generated successfully!")
        print(f"  Saved to: dev/financial_erd.png")
        print(f"  Graphviz object: {type(erd)}")
    except Exception as e:
        print(f"✗ ERD generation failed: {e}")
        import traceback
        traceback.print_exc()

    print()


def test_eda():
    """Test EDA functions."""
    print("=" * 80)
    print("Testing EDA Functions")
    print("=" * 80)

    # Load sample data
    data, metadata = download_demo(
        modality='multi_table',
        dataset_name='financial_v1'
    )

    # Test dataset summary
    try:
        print_dataset_summary(data, metadata)
        print("\n✓ Dataset summary printed successfully!")
    except Exception as e:
        print(f"✗ Dataset summary failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n")

    # Test table exploration
    try:
        explore_table(data, 'account')
        print("\n✓ Table exploration successful!")
    except Exception as e:
        print(f"✗ Table exploration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_erd()
    print("\n" * 2)
    test_eda()
