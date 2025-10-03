"""Inspect SDV metadata structure."""

from sdv.datasets.demo import download_demo

data, metadata = download_demo(
    modality='multi_table',
    dataset_name='financial_v1'
)

print("Metadata type:", type(metadata))
print("\nMetadata attributes:", dir(metadata))
print("\nMetadata dict:", metadata.to_dict())
