import sys
import traceback
from pathlib import Path

try:
    import win32com.client
except ImportError:
    win32com = None


ROOT_DIR = Path(__file__).resolve().parents[2]
WORKBOOK_CANDIDATES = [
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def resolve_workbook() -> Path:
    for path in WORKBOOK_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Nenhum workbook principal encontrado: OPERACOES_E_OPCOES.xlsm/xlsx"
    )


def main() -> int:
    try:
        log("INFO", "Iniciando check local do runtime Excel")

        if win32com is None:
            raise RuntimeError("pywin32 não instalado. Execute: python -m pip install pywin32")

        workbook_path = resolve_workbook()
        log("INFO", f"Workbook localizado: {workbook_path}")

        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        log("OK", "Excel COM iniciado com sucesso")

        wb = excel.Workbooks.Open(str(workbook_path))
        log("OK", f"Workbook aberto: {wb.Name}")

        sheet_count = wb.Worksheets.Count
        log("INFO", f"Quantidade de abas: {sheet_count}")

        if sheet_count <= 0:
            raise ValueError("Workbook sem abas disponíveis")

        first_sheet = wb.Worksheets(1)
        a1 = first_sheet.Cells(1, 1).Value
        log("INFO", f"Primeira aba: {first_sheet.Name} | A1={a1}")

        wb.Close(SaveChanges=False)
        excel.Quit()

        log("OK", "Check de Excel local concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check de Excel local: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
