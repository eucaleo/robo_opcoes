"""
Conecta automaticamente na instância do Excel que tem o workbook
LISTA_RTD.xlsm aberto, independente de quantos Excel estejam rodando.
"""
import sys
import win32com.client
import pythoncom

TARGET_FILE = "LISTA_RTD.xlsm"


def find_workbook(target_name=TARGET_FILE):
    """Procura no ROT (Running Object Table) o workbook alvo."""
    context = pythoncom.CreateBindCtx(0)
    rot = pythoncom.GetRunningObjectTable()

    for moniker in rot:
        try:
            name = moniker.GetDisplayName(context, None)
        except Exception:
            continue

        if target_name.lower() in name.lower():
            try:
                obj = rot.GetObject(moniker)
                wb = win32com.client.Dispatch(
                    obj.QueryInterface(pythoncom.IID_IDispatch)
                )
                return wb, name
            except Exception as e:
                print(f"⚠️  Encontrou moniker mas falhou ao conectar: {e}")
                continue

    return None, None


def connect():
    wb, path = find_workbook()

    if wb is None:
        print(f"❌ Não achou nenhuma instância com {TARGET_FILE} aberto.")
        sys.exit(1)

    app = wb.Application
    print(f"✅ Conectado: {wb.Name}")
    print(f"   Caminho: {path}")
    print(f"   PID do Excel (via Hwnd): {app.Hwnd}")
    print(f"   Visible: {app.Visible}")
    print(f"   Workbooks abertos nesta instância: {app.Workbooks.Count}")

    return wb, app


if __name__ == "__main__":
    wb, app = connect()

    # Exemplo de uso: acessar uma planilha e ler uma célula
    try:
        sheet = wb.Sheets(1)
        print(f"   Primeira aba: {sheet.Name}")
        print(f"   Célula A1: {sheet.Range('A1').Value}")
    except Exception as e:
        print(f"⚠️  Erro ao ler dados da planilha: {e}")
