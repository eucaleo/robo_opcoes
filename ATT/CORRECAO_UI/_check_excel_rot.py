import win32com.client
import pythoncom
import win32process

def get_pid_from_hwnd(hwnd):
    try:
        _thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception:
        return None

context = pythoncom.CreateBindCtx(0)
rot = pythoncom.GetRunningObjectTable()

found_any = False

print("=" * 70)
print("VARREDURA DO ROT (Running Object Table) - Instancias Excel")
print("=" * 70)

for moniker in rot:
    try:
        name = moniker.GetDisplayName(context, None)
    except Exception:
        continue

    if "Excel" not in name and ".xls" not in name.lower():
        continue

    found_any = True
    print("\nMoniker: " + name)

    try:
        obj = rot.GetObject(moniker)
        idisp = obj.QueryInterface(pythoncom.IID_IDispatch)
        disp = win32com.client.Dispatch(idisp)

        wb_name = getattr(disp, "Name", None)
        wb_full = getattr(disp, "FullName", None)
        print("  Nome do objeto: " + str(wb_name))
        print("  Caminho completo: " + str(wb_full))

        try:
            app = disp.Application
            pid = get_pid_from_hwnd(app.Hwnd)
            print("  Application.Hwnd: " + str(app.Hwnd))
            print("  PID do processo: " + str(pid))
            print("  Application.Visible: " + str(app.Visible))
            print("  Workbooks.Count nessa instancia: " + str(app.Workbooks.Count))
            for wb in app.Workbooks:
                print("    -> Workbook aberto: " + wb.Name + " | " + wb.FullName)
        except Exception as e:
            print("  [AVISO] Nao foi possivel obter Application/PID: " + str(e))

    except Exception as e:
        print("  [ERRO] Falha ao acessar objeto do moniker: " + str(e))

if not found_any:
    print("\nNenhuma instancia Excel encontrada no ROT.")
    print("Isso significa que NENHUM Excel esta registrado como 'ativo'")
    print("para automacao COM neste momento (mesmo que o processo exista")
    print("no Gerenciador de Tarefas).")

print("\n" + "=" * 70)
print("FIM DA VARREDURA")
print("=" * 70)
