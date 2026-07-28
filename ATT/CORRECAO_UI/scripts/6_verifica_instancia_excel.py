import subprocess
import sys
import time

def contar_excel():
    """Conta processos EXCEL.EXE ativos (Windows)."""
    try:
        saida = subprocess.check_output(
            'tasklist /FI "IMAGENAME eq EXCEL.EXE"',
            shell=True, text=True, errors="ignore"
        )
        return saida.count("EXCEL.EXE")
    except Exception:
        return -1

def matar_excel_orfaos():
    """Mata processos EXCEL.EXE remanescentes (usar com cautela)."""
    subprocess.call('taskkill /F /IM EXCEL.EXE /T', shell=True)

if __name__ == "__main__":
    ESPERA_SEGUNDOS = int(sys.argv[1]) if len(sys.argv) > 1 else 15

    print("=== VERIFICACAO DE INSTANCIA EXCEL (antes/depois) ===\n")

    antes = contar_excel()
    print(f"Processos EXCEL.EXE ANTES do teste: {antes}")

    print(f"\n>> Aguardando {ESPERA_SEGUNDOS}s para o sistema abrir/operar/fechar o Excel...")
    time.sleep(ESPERA_SEGUNDOS)

    depois = contar_excel()
    print(f"\nProcessos EXCEL.EXE DEPOIS da espera: {depois}")

    if depois > antes:
        print(f"\n[RISCO] {depois - antes} processo(s) EXCEL.EXE ficaram ORFAOS/OCULTOS.")
        print("-> Verificar liberacao de referencia COM (win32com/xlwings) no encerramento.")
    elif depois == antes:
        print("\n[OK] Nenhum processo Excel adicional ficou preso. Fechamento limpo.")
    else:
        print("\n[ATENCAO] Menos processos depois que antes - verificar fechamento indevido.")
