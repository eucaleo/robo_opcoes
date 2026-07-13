import sys
import csv
import traceback
from io import StringIO
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
BRIDGE_DIR = ROOT_DIR / "bridge"

CSV_CANDIDATES = [
    BRIDGE_DIR / "analise_robo_legs.csv",
    BRIDGE_DIR / "analise_robo.csv",
    BRIDGE_DIR / "analise_raiox.csv",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def read_text_with_fallback(path: Path) -> tuple[str, str]:
    data = path.read_bytes()

    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return data.decode("latin-1", errors="replace"), "latin-1-replace"


def read_csv_rows(path: Path):
    text, encoding = read_text_with_fallback(path)
    sample = text[:4096]

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
        delimiter = dialect.delimiter
        rows = list(csv.reader(StringIO(text), dialect))
    except csv.Error:
        first_line = sample.splitlines()[0] if sample.splitlines() else ""
        delimiter = "," if first_line.count(",") > first_line.count(";") else ";"
        rows = list(csv.reader(StringIO(text), delimiter=delimiter))

    return rows, delimiter, encoding


def validate_csv(path: Path) -> None:
    rows, delimiter, encoding = read_csv_rows(path)

    if not rows:
        raise ValueError(f"CSV vazio: {path}")

    headers = rows[0]
    log("INFO", f"CSV validado: {path.name}")
    log("INFO", f"Encoding detectado: {encoding}")
    log("INFO", f"Delimitador detectado: {delimiter!r}")
    log("INFO", f"Colunas detectadas: {headers[:20]}")
    log("INFO", f"Quantidade de linhas incluindo cabeçalho: {len(rows)}")

    if len(headers) <= 1:
        raise ValueError(
            f"CSV parece não ter sido interpretado corretamente: apenas {len(headers)} coluna(s)"
        )


def main() -> int:
    try:
        log("INFO", "Iniciando check de legs real do projeto")

        found_csv = False
        for path in CSV_CANDIDATES:
            if path.exists():
                validate_csv(path)
                found_csv = True

        if not found_csv:
            raise FileNotFoundError("Nenhum CSV real de legs/estrutura foi encontrado")

        log("OK", "check_legs concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_legs: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
