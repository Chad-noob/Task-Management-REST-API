from pathlib import Path

from .database import get_connection


def initialize_database() -> None:
    """Create tables if they are missing."""
    project_root = Path(__file__).resolve().parent.parent
    schema_file = project_root / 'schema.sql'

    with get_connection() as connection:
        connection.executescript(schema_file.read_text(encoding='utf-8'))
        connection.commit()
