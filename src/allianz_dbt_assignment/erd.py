"""Entity Relationship Diagram generation from SDV metadata."""

from typing import Any

try:
    import graphviz
except ImportError:
    graphviz = None


def generate_erd(metadata: dict[str, Any] | Any, output_path: str | None = None) -> Any:
    """
    Generate an ERD from SDV metadata.

    Args:
        metadata: SDV metadata dictionary or Metadata object containing tables and relationships
        output_path: Optional path to save the diagram (without extension)

    Returns:
        Graphviz Digraph object that can be displayed in Jupyter
    """
    if graphviz is None:
        raise ImportError("graphviz package required. Install with: pip install graphviz")

    # Convert Metadata object to dict if needed
    if hasattr(metadata, 'to_dict'):
        metadata = metadata.to_dict()

    dot = graphviz.Digraph(comment='ERD', format='png')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='plaintext')

    # Add tables as nodes with HTML-like labels
    for table_name, table_info in metadata['tables'].items():
        columns = table_info['columns']
        pk = table_info.get('primary_key', '')

        # Build HTML table for node
        label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        label += f'<TR><TD BGCOLOR="lightblue"><B>{table_name}</B></TD></TR>'

        for col_name, col_info in columns.items():
            sdtype = col_info.get('sdtype', '')
            pk_marker = ' 🔑' if col_name == pk else ''
            label += f'<TR><TD ALIGN="LEFT">{col_name}{pk_marker} ({sdtype})</TD></TR>'

        label += '</TABLE>>'
        dot.node(table_name, label)

    # Add relationships as edges
    for rel in metadata.get('relationships', []):
        parent = rel['parent_table_name']
        child = rel['child_table_name']
        parent_key = rel['parent_primary_key']
        child_key = rel['child_foreign_key']

        dot.edge(
            parent,
            child,
            label=f'{parent_key} → {child_key}',
            dir='forward'
        )

    if output_path:
        dot.render(output_path, cleanup=True)

    return dot
