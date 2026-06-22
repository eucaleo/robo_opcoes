#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3e-fix2-patch-direto-facade-manual-sem-alias.txt"

mkdir -p "$EVID_DIR"
mkdir -p "ATT/tests"

{
  echo "== Fase 3E fix2 - patch direto facade manual sem alias =="
  date
  echo
  echo "Branch:"
  git branch --show-current || true
  echo
  echo "Status inicial:"
  git status --short || true
  echo
} > "$OUT"

python - <<'PY' >> "$OUT" 2>&1
from pathlib import Path
import re
import textwrap

facade_path = Path("services/canonical_pricing_facade.py")
ui_path = Path("UI/main_window.py")
test_path = Path("ATT/tests/test_canonical_pricing_facade_manual_without_alias.py")

if not facade_path.exists():
    raise SystemExit(f"Arquivo não encontrado: {facade_path}")

facade = facade_path.read_text(encoding="utf-8")

backup = facade_path.with_suffix(".py.fase3e.fix2.bak")
if not backup.exists():
    backup.write_text(facade, encoding="utf-8")
    print(f"Backup criado: {backup}")

print("Aplicando patch direto em services/canonical_pricing_facade.py")

# -------------------------------------------------------------------
# 1) Garante import do PricingInputService
# -------------------------------------------------------------------
if "PricingInputService" not in facade:
    import_anchor_candidates = [
        "from services.pricing_execution_service import PricingExecutionService\n",
        "from services.pricing_execution_persistence_service import PricingExecutionPersistenceService\n",
    ]

    inserted = False
    for anchor in import_anchor_candidates:
        if anchor in facade:
            facade = facade.replace(
                anchor,
                anchor + "from services.pricing_input_service import PricingInputService\n",
                1,
            )
            inserted = True
            print("Import PricingInputService adicionado via anchor.")
            break

    if not inserted:
        # fallback: adiciona depois dos imports iniciais
        lines = facade.splitlines(True)
        last_import_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                last_import_idx = i
        if last_import_idx < 0:
            raise SystemExit("Não foi possível localizar bloco de imports.")
        lines.insert(last_import_idx + 1, "from services.pricing_input_service import PricingInputService\n")
        facade = "".join(lines)
        print("Import PricingInputService adicionado após último import.")
else:
    print("PricingInputService já aparece no arquivo.")

# -------------------------------------------------------------------
# 2) Substitui o método execute_pricing inteiro
# -------------------------------------------------------------------
new_method = '''    def execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        started_at = time.perf_counter()

        try:
            # 1. Monta pricing_payload.
            #
            # Caminho A - legado/captura:
            #   structures.alias_legacy_aba preenchido -> MarketSnapshotSelector.
            #
            # Caminho B - manual canônico:
            #   structures.alias_legacy_aba NULL -> PricingInputService.build_pricing_payload().
            #
            # O caminho B corrige estruturas cadastradas manualmente pela UI.
            try:
                aba, underlying_asset = _get_structure_info(
                    structure_id,
                    self._db_path,
                )

                selection = self._selector.select(aba=aba)

                pricing_payload = _snapshot_result_to_payload(
                    selection_result=selection,
                    structure_id=structure_id,
                    underlying_asset=underlying_asset,
                    reference_date=reference_date,
                    db_path=self._db_path,
                )

            except ValueError as exc:
                message = str(exc)

                if "alias_legacy_aba is null" not in message:
                    raise

                try:
                    pricing_input_service = PricingInputService(db_path=self._db_path)
                except TypeError:
                    pricing_input_service = PricingInputService()

                try:
                    pricing_payload = pricing_input_service.build_pricing_payload(
                        structure_id=structure_id,
                        reference_date=reference_date,
                    )
                except TypeError:
                    pricing_payload = pricing_input_service.build_pricing_payload(
                        structure_id=structure_id,
                    )

                if not isinstance(pricing_payload, dict):
                    raise ValueError(
                        "PricingInputService.build_pricing_payload() retornou payload inválido"
                    )

                pricing_payload.setdefault("structure_id", structure_id)

                if reference_date is not None:
                    pricing_payload.setdefault("reference_date", reference_date)

                meta = pricing_payload.get("meta")
                if not isinstance(meta, dict):
                    meta = {}
                    pricing_payload["meta"] = meta

                meta.setdefault("snapshot_source", "canonical_manual_without_alias")
                meta.setdefault("alias_legacy_aba", None)
                meta.setdefault("fallback_reason", message.strip())

            # 2. Executa engine
            execution_result = self._engine.execute_payload(
                pricing_payload=pricing_payload,
            )

            # C4: extrai dict interno do wrapper
            engine_result = execution_result.get("result", execution_result)

            duration_ms = int((time.perf_counter() - started_at) * 1000)

            # 3. Persiste app.db + derived.db via port
            persisted = self._persister.persist_execution(
                pricing_payload=pricing_payload,
                result=engine_result,
                duration_ms=duration_ms,
                error_message=None,
            )

            return {
                "status":          "ok",
                "canonical_input": pricing_payload,
                "pricing_payload": pricing_payload,
                "result":          execution_result,
                "persisted":       persisted,
                "meta":            pricing_payload.get("meta", {}),
                "duration_ms":     duration_ms,
            }

        except Exception as exc:
            duration_ms   = int((time.perf_counter() - started_at) * 1000)
            error_message = str(exc)

            try:
                self._persister.persist_execution(
                    pricing_payload=None,
                    result={"engine": "stub", "status": "error", "error_message": error_message},
                    duration_ms=duration_ms,
                    error_message=error_message,
                )
            except Exception:
                pass

            return {
                "status":          "error",
                "canonical_input": None,
                "pricing_payload": None,
                "result":          None,
                "persisted":       None,
                "meta":            {},
                "duration_ms":     duration_ms,
                "error_message":   error_message,
            }
'''

pattern = re.compile(
    r"    def execute_pricing\(\n"
    r"        self,\n"
    r"        structure_id: int,\n"
    r"        reference_date: str \| None = None,\n"
    r"    \) -> dict\[str, Any\]:\n"
    r".*?"
    r"(?=\n    def |\Z)",
    re.DOTALL,
)

facade2, n = pattern.subn(new_method, facade, count=1)

if n != 1:
    raise SystemExit("Não foi possível substituir execute_pricing por regex.")

facade_path.write_text(facade2, encoding="utf-8")
print("execute_pricing substituído com fallback manual sem alias.")

# -------------------------------------------------------------------
# 3) Patch UI: não mascarar status=error
# -------------------------------------------------------------------
if ui_path.exists():
    ui = ui_path.read_text(encoding="utf-8")
    ui_backup = ui_path.with_suffix(".py.fase3e.fix2.bak")
    if not ui_backup.exists():
        ui_backup.write_text(ui, encoding="utf-8")
        print(f"Backup criado: {ui_backup}")

    if "facade.execute_pricing(sid)" in ui and "Erro no recálculo automático" not in ui:
        ui = ui.replace(
            "                facade.execute_pricing(sid)\n",
            '''                result = facade.execute_pricing(sid)

                if isinstance(result, dict) and result.get("status") == "error":
                    raise RuntimeError(
                        result.get("error_message") or "Erro no recálculo automático"
                    )
''',
            1,
        )
        ui_path.write_text(ui, encoding="utf-8")
        print("UI ajustada para não mascarar status=error.")
    else:
        print("UI não alterada: trecho já ajustado ou anchor não encontrado.")
else:
    print(f"UI não encontrada: {ui_path}")

# -------------------------------------------------------------------
# 4) Teste de regressão
# -------------------------------------------------------------------
test_code = '''import services.canonical_pricing_facade as facade_module


class FakePricingInputService:
    def __init__(self, *args, **kwargs):
        pass

    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        return {
            "structure_id": structure_id,
            "underlying_asset": "BOVA11",
            "reference_date": reference_date,
            "spot_price": 124.66,
            "interest_rate": 0.0,
            "volatility": 0.0,
            "legs": [],
            "meta": {
                "source": "fake_pricing_input_service",
            },
        }


class FakePricingExecutionService:
    def execute_payload(self, pricing_payload):
        return {
            "result": {
                "engine": "fake",
                "status": "ok",
                "valuation": {
                    "theoretical_value": 0,
                },
            }
        }


class FakePersistenceService:
    def __init__(self):
        self.calls = []

    def persist_execution(
        self,
        pricing_payload,
        result,
        duration_ms=None,
        error_message=None,
    ):
        self.calls.append(
            {
                "pricing_payload": pricing_payload,
                "result": result,
                "duration_ms": duration_ms,
                "error_message": error_message,
            }
        )
        return {
            "ok": True,
            "structure_id": pricing_payload["structure_id"] if pricing_payload else None,
        }


def test_facade_falls_back_to_pricing_input_service_when_alias_legacy_aba_is_null(monkeypatch, tmp_path):
    def fake_get_structure_info(structure_id, db_path):
        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")

    monkeypatch.setattr(
        facade_module,
        "_get_structure_info",
        fake_get_structure_info,
    )

    monkeypatch.setattr(
        facade_module,
        "PricingInputService",
        FakePricingInputService,
    )

    persister = FakePersistenceService()

    facade = facade_module.CanonicalPricingFacade(
        db_path=tmp_path / "app.db",
        pricing_execution_service=FakePricingExecutionService(),
        persistence_service=persister,
    )

    response = facade.execute_pricing(
        structure_id=2,
        reference_date="2026-06-21",
    )

    assert response["status"] == "ok"
    assert response["pricing_payload"]["structure_id"] == 2
    assert response["pricing_payload"]["reference_date"] == "2026-06-21"
    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
    assert response["pricing_payload"]["meta"]["alias_legacy_aba"] is None
    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]

    assert len(persister.calls) == 1
    assert persister.calls[0]["pricing_payload"]["structure_id"] == 2
    assert persister.calls[0]["result"]["status"] == "ok"
'''

test_path.write_text(test_code, encoding="utf-8")
print(f"Teste criado: {test_path}")
PY

{
  echo
  echo "== Diff =="
  git diff -- services/canonical_pricing_facade.py UI/main_window.py ATT/tests/test_canonical_pricing_facade_manual_without_alias.py || true

  echo
  echo "== Py compile =="
  python -m py_compile services/canonical_pricing_facade.py
  if [ -f UI/main_window.py ]; then
    python -m py_compile UI/main_window.py
  fi
  python -m py_compile ATT/tests/test_canonical_pricing_facade_manual_without_alias.py
  echo "py_compile OK"

  echo
  echo "== Pytest regressao =="
  python -m pytest -q ATT/tests/test_canonical_pricing_facade_manual_without_alias.py

  echo
  echo "== Status final =="
  git status --short

  echo
  echo "== Fim fix2 =="
} >> "$OUT" 2>&1

cat "$OUT"
