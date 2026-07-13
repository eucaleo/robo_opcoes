from pathlib import Path
import importlib


def test_rtd_excel_online_importa_do_pacote_raiz():
    root = Path(__file__).resolve().parents[2]
    pacote_raiz = (root / "rtd_excel_online").resolve()

    pkg = importlib.import_module("rtd_excel_online")
    mod = importlib.import_module("rtd_excel_online.fase7_alertas_decisao")

    assert Path(pkg.__file__).resolve().is_relative_to(pacote_raiz)
    assert Path(mod.__file__).resolve().is_relative_to(pacote_raiz)


def test_nao_existe_pacote_duplicado_em_src():
    root = Path(__file__).resolve().parents[2]

    assert not (root / "src" / "rtd_excel_online").exists()
