"""
Data exploration package for DBT case study.

This package contains modules for exploring DuckDB tables including:
- ID analysis
- Descriptive statistics
- Outlier detection
- Data quality analysis
- Data cleaning
- Visualization
- Relationship validation
"""

from allianz_dbt_assignment.data_exploration.id_analyzer import IDAnalyzer
from allianz_dbt_assignment.data_exploration.descriptive_stats import DescriptiveStats
from allianz_dbt_assignment.data_exploration.outlier_detection import OutlierDetector
from allianz_dbt_assignment.data_exploration.data_quality import DataQualityAnalyzer
from allianz_dbt_assignment.data_exploration.data_cleaner import DataCleaner
from allianz_dbt_assignment.data_exploration.plotting import Plotter
from allianz_dbt_assignment.data_exploration.utils import execute_query
from allianz_dbt_assignment.data_exploration.relationship_validator import RelationshipValidator

__all__ = [
    'IDAnalyzer',
    'DescriptiveStats',
    'OutlierDetector',
    'DataQualityAnalyzer',
    'DataCleaner',
    'Plotter',
    'execute_query',
    'RelationshipValidator'
]

