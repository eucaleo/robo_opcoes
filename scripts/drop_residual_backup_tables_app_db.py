from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from db.config import connect_app  # noqa: E402


RESIDUAL_TABLES = [
    "rtd_option_quotes_backup_scope_20260626_184057",
]


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def main() -> None:
    with connect_app() as conn:
        for table_name in RESIDUAL_TABLES:
            conn.execute(f"DROP TABLE IF EXISTS {_quote_identifier(table_name)}")
        conn.commit()


if __name__ == "__main__":
    main()
