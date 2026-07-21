from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_method(path: Path, method_name: str, new_source: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"    def {method_name}("):
            start = i
            break

    if start is None:
        return False

    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if line.startswith("    def ") or line.startswith("class "):
            end = j
            break

    new_lines = new_source.splitlines(keepends=True)
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"

    lines[start:end] = new_lines
    path.write_text("".join(lines), encoding="utf-8")
    return True


def insert_before_method(path: Path, marker_method: str, source: str, id_token: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if id_token in text:
        return False

    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith(f"    def {marker_method}("):
            block = source
            if not block.endswith("\n"):
                block += "\n"
            lines.insert(i, block + "\n")
            path.write_text("".join(lines), encoding="utf-8")
            return True

    return False


def patch_terminal_dark_panel() -> None:
    path = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
    if not path.exists():
        print(f"SKIP: {path} nao encontrado")
        return

    helpers = '''    def _selected_structure_id_for_backend_refresh(self, structure: object) -> int:
        """
        Extrai structure_id da estrutura aberta em tela.

        A UI apenas identifica a estrutura. O cálculo permanece no backend.
        """
        sid = None

        if isinstance(structure, dict):
            sid = (
                structure.get("structure_id")
                or structure.get("id")
                or structure.get("sid")
            )
        else:
            sid = (
                getattr(structure, "structure_id", None)
                or getattr(structure, "id", None)
                or getattr(structure, "sid", None)
            )

        if sid is None:
            raise ValueError("structure_id ausente na estrutura selecionada")

        return int(sid)

    def _invalidate_payoff_ui_caches_for_structure(self, structure_id: int) -> None:
        """
        Invalida caches locais da UI depois do comando oficial.

        Não recalcula nada. Apenas evita gráfico velho.
        """
        owners = [
            self,
            getattr(self, "app_service", None),
            getattr(self, "service", None),
            getattr(self, "data_model", None),
        ]

        for owner in owners:
            if owner is None:
                continue

            invalidator = getattr(owner, "invalidate_payoff_cache", None)
            if callable(invalidator):
                try:
                    invalidator(structure_id)
                except TypeError:
                    invalidator()
                except Exception:
                    pass

            for attr in (
                "_payoff_cache",
                "payoff_cache",
                "_viewmodel_cache",
                "viewmodel_cache",
            ):
                cache = getattr(owner, attr, None)
                if isinstance(cache, dict):
                    cache.clear()

    def _refresh_open_structure_payoff_via_backend(self, action_label: str) -> dict:
        """
        Solicita refresh/recalculo da estrutura aberta ao backend oficial.

        Fluxo:
        UI -> PayoffRefreshCommandService -> PricingExecutionAppService
        """
        structure = self._require_active_selected_structure(action_label)
        structure_id = self._selected_structure_id_for_backend_refresh(structure)

        self._safe_status(
            f"Solicitando {action_label} da estrutura {structure_id} ao backend..."
        )

        from services.payoff_refresh_command_service import PayoffRefreshCommandService

        result = PayoffRefreshCommandService().refresh_payoff_for_structure(
            structure_id
        )

        self._invalidate_payoff_ui_caches_for_structure(structure_id)
        return result

    def refresh_selected_structure_payoff(self) -> None:
        """
        Handler semântico para o botão Atualizar payoff.

        Mantém o gráfico da estrutura aberta alinhado ao snapshot persistido
        mais recente, sem cálculo local na UI.
        """
        self.recalculate_selected_structure()
'''

    insert_before_method(
        path=path,
        marker_method="recalculate_selected_structure",
        source=helpers,
        id_token="_refresh_open_structure_payoff_via_backend",
    )

    new_method = '''    def recalculate_selected_structure(self) -> None:
        """
        Compatibilidade de nome legado.

        Semântica atual:
        - botão Atualizar payoff;
        - somente estrutura aberta em tela;
        - cálculo executado pelo backend oficial;
        - UI apenas invalida cache, relê snapshot persistido e redesenha.
        """
        try:
            result = self._refresh_open_structure_payoff_via_backend(
                "atualizar payoff"
            )

            ok = self._refresh_selected_structure_from_store(silent=False)

            status = str(result.get("status") or "").lower()
            ts = result.get("latest_payoff_timestamp")
            points = result.get("payoff_points_count")

            if ok:
                self._safe_status(
                    f"Payoff atualizado via backend: status={status}, "
                    f"pontos={points}, timestamp={ts}"
                )
            else:
                self._safe_status(
                    "Backend executado, mas a UI não conseguiu reler "
                    "o snapshot persistido."
                )

        except Exception as exc:
            self._safe_status(f"Erro ao atualizar payoff: {exc}")
            messagebox.showerror(
                "Erro ao atualizar payoff",
                str(exc),
                parent=self.winfo_toplevel(),
            )
'''

    changed = replace_method(path, "recalculate_selected_structure", new_method)
    print(f"terminal_vwap_payoff_dark_panel.py recalculate_selected_structure: {changed}")


def patch_main_window() -> None:
    path = ROOT / "UI" / "main_window.py"
    if not path.exists():
        print(f"SKIP: {path} nao encontrado")
        return

    new_method = '''    def recalculate_structure(self, structure_id: str):
        """
        Recalcula somente a estrutura informada usando o backend oficial.

        A UI não calcula payoff nem decisão.
        """
        try:
            sid = int(structure_id)

            if hasattr(self, "status_bar"):
                self.status_bar.config(
                    text=f"Solicitando recalculo da estrutura {sid} ao backend..."
                )

            from services.payoff_refresh_command_service import PayoffRefreshCommandService

            result = PayoffRefreshCommandService().refresh_payoff_for_structure(sid)

            data_model = getattr(self, "data_model", None)
            if data_model is not None:
                invalidator = getattr(data_model, "invalidate_payoff_cache", None)
                if callable(invalidator):
                    try:
                        invalidator(sid)
                    except TypeError:
                        invalidator()
                elif hasattr(data_model, "_payoff_cache"):
                    try:
                        data_model._payoff_cache.clear()
                    except Exception:
                        pass

            if hasattr(self, "refresh_data"):
                self.refresh_data()

            status = str(result.get("status") or "").lower()
            ts = result.get("latest_payoff_timestamp")
            points = result.get("payoff_points_count")

            if hasattr(self, "status_bar"):
                self.status_bar.config(
                    text=(
                        f"Recalculo da estrutura {sid} concluido: "
                        f"status={status}, pontos={points}, timestamp={ts}"
                    )
                )

            return result

        except Exception as exc:
            if hasattr(self, "status_bar"):
                self.status_bar.config(
                    text=f"Erro ao recalcular estrutura: {exc}"
                )
            raise
'''

    changed = replace_method(path, "recalculate_structure", new_method)
    print(f"main_window.py recalculate_structure: {changed}")


def patch_ui_data_cache_api() -> None:
    path = ROOT / "UI" / "models" / "ui_data.py"
    if not path.exists():
        print(f"SKIP: {path} nao encontrado")
        return

    text = path.read_text(encoding="utf-8")
    if "def invalidate_payoff_cache(" in text:
        print("ui_data.py invalidate_payoff_cache: ja existe")
        return

    method = '''    def invalidate_payoff_cache(self, structure_id=None) -> None:
        """
        Invalida cache local de payoff.

        A UI usa isso apos comando oficial de backend para evitar
        leitura de snapshot antigo.
        """
        if hasattr(self, "_payoff_cache") and isinstance(self._payoff_cache, dict):
            self._payoff_cache.clear()

'''

    lines = text.splitlines(keepends=True)

    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("    def ") and "_payoff_cache" in "".join(lines[max(0, i - 20):i + 20]):
            insert_at = i
            break

    if insert_at is None:
        for i, line in enumerate(lines):
            if line.startswith("class "):
                insert_at = i + 1
                break

    if insert_at is None:
        print("ui_data.py invalidate_payoff_cache: ponto de insercao nao encontrado")
        return

    lines.insert(insert_at, method)
    path.write_text("".join(lines), encoding="utf-8")
    print("ui_data.py invalidate_payoff_cache: inserido")


def main() -> None:
    patch_terminal_dark_panel()
    patch_main_window()
    patch_ui_data_cache_api()


if __name__ == "__main__":
    main()
