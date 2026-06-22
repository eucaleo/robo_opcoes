#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3e-fix-facade-manual-sem-alias.txt"

mkdir -p "$EVID_DIR"

echo "== Fase 3E - fix facade manual sem alias legado ==" > "$OUT"
echo >> "$OUT"
date >> "$OUT"
echo >> "$OUT"

echo "1) Estado inicial git" >> "$OUT"
git branch --show-current >> "$OUT" 2>&1 || true
git status --short >> "$OUT" 2>&1 || true
git log --oneline -8 >> "$OUT" 2>&1 || true
echo >> "$OUT"

python - <<'PY' >> "$OUT" 2>&1
from pathlib import Path
import re
import textwrap

print("2) Aplicando patches Python/textuais")
print()

facade_path = Path("services/canonical_pricing_facade.py")
ui_path = Path("UI/main_window.py")
test_path = Path("ATT/tests/test_canonical_pricing_facade_manual_without_alias.py")

if not facade_path.exists():
    raise SystemExit(f"Arquivo não encontrado: {facade_path}")

if not ui_path.exists():
    raise SystemExit(f"Arquivo não encontrado: {ui_path}")

facade = facade_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")

# ------------------------------------------------------------------
# Backup simples
# ------------------------------------------------------------------
backup_facade = facade_path.with_suffix(".py.fase3e.bak")
backup_ui = ui_path.with_suffix(".py.fase3e.bak")

if not backup_facade.exists():
    backup_facade.write_text(facade, encoding="utf-8")
    print(f"Backup criado: {backup_facade}")

if not backup_ui.exists():
    backup_ui.write_text(ui, encoding="utf-8")
    print(f"Backup criado: {backup_ui}")

# ------------------------------------------------------------------
# Patch 1: import PricingInputService
# ------------------------------------------------------------------
import_line = "from services.pricing_input_service import PricingInputService\n"

if import_line not in facade:
    anchor = "from services.pricing_execution_service import PricingExecutionService\n"
    if anchor not in facade:
        raise SystemExit("Anchor de import não encontrado em canonical_pricing_facade.py")
    facade = facade.replace(anchor, anchor + import_line)
    print("Import adicionado: PricingInputService")
else:
    print("Import PricingInputService já existente")

# ------------------------------------------------------------------
# Patch 2: inicializa PricingInputService no __init__
# ------------------------------------------------------------------
engine_line = "        self._engine   = pricing_execution_service or PricingExecutionService()\n"

pricing_input_block = """        try:
            self._pricing_input_service = PricingInputService(db_path=self._db_path)
        except TypeError:
            # Compatibilidade com versões em que PricingInputService não recebe db_path.
            self._pricing_input_service = PricingInputService()

"""

if "_pricing_input_service" not in facade:
    if engine_line not in facade:
        raise SystemExit("Anchor self._engine não encontrado em canonical_pricing_facade.py")
    facade = facade.replace(engine_line, engine_line + "\n" + pricing_input_block)
    print("Inicialização _pricing_input_service adicionada")
else:
    print("_pricing_input_service já existente")

# ------------------------------------------------------------------
# Patch 3: adiciona método _build_pricing_payload_for_structure
# ------------------------------------------------------------------
helper_method = '''    def _build_pricing_payload_for_structure(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Monta o pricing_payload para a estrutura.

        Caminhos suportados:
          1. Legado/captura: quando structures.alias_legacy_aba existe,
             usa MarketSnapshotSelector manual > rtd.
          2. Manual canônico: quando alias_legacy_aba é NULL,
             usa PricingInputService.build_pricing_payload(), sem exigir aba legada.

        Esse fallback é necessário para estruturas criadas manualmente na UI.
        """
        try:
            aba, underlying_asset = _get_structure_info(
                structure_id,
                self._db_path,
            )
        except ValueError as exc:
            message = str(exc)

            if "alias_legacy_aba is null" not in message:
                raise

            pricing_payload = self._pricing_input_service.build_pricing_payload(
                structure_id=structure_id,
                reference_date=reference_date,
            )

            if not isinstance(pricing_payload, dict):
                raise ValueError(
                    "PricingInputService.build_pricing_payload() retornou payload inválido"
                )

            pricing_payload.setdefault("structure_id", structure_id)
            pricing_payload.setdefault("reference_date", reference_date)

            meta = pricing_payload.get("meta")
            if not isinstance(meta, dict):
                meta = {}
                pricing_payload["meta"] = meta

            meta.setdefault("snapshot_source", "canonical_manual_without_alias")
            meta.setdefault("alias_legacy_aba", None)
            meta.setdefault("fallback_reason", message)

            return pricing_payload

        selection = self._selector.select(aba=aba)

        return _snapshot_result_to_payload(
            selection_result=selection,
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            reference_date=reference_date,
            db_path=self._db_path,
        )

'''

if "def _build_pricing_payload_for_structure(" not in facade:
    anchor = "    def execute_pricing(\n"
    if anchor not in facade:
        raise SystemExit("Anchor def execute_pricing não encontrado")
    facade = facade.replace(anchor, helper_method + "\n" + anchor)
    print("Método _build_pricing_payload_for_structure adicionado")
else:
    print("Método _build_pricing_payload_for_structure já existente")

# ------------------------------------------------------------------
# Patch 4: troca passos 1/2/3 de execute_pricing pelo helper
# ------------------------------------------------------------------
old_block = '''            #  1. Resolve aba + underlying_asset
            aba, underlying_asset = _get_structure_info(   #  C6/C8
                structure_id, self._db_path
            )

            #  2. Seleciona snapshot (manual > rtd)
            selection = self._selector.select(aba=aba)

            #  3. Monta pricing_payload
            pricing_payload = _snapshot_result_to_payload(
                selection_result=selection,
                structure_id=structure_id,
                underlying_asset=underlying_asset,          #  C7/C8
                reference_date=reference_date,
                db_path=self._db_path,
            )
'''

new_block = '''            #  1. Monta pricing_payload
            #     - legado: alias_legacy_aba -> MarketSnapshotSelector
            #     - manual canônico: alias_legacy_aba NULL -> PricingInputService
            pricing_payload = self._build_pricing_payload_for_structure(
                structure_id=structure_id,
                reference_date=reference_date,
            )
'''

if old_block in facade:
    facade = facade.replace(old_block, new_block, 1)
    print("execute_pricing ajustado para usar helper/fallback")
else:
    if "self._build_pricing_payload_for_structure(" in facade:
        print("execute_pricing aparentemente já usa helper/fallback")
    else:
        raise SystemExit("Bloco antigo de execute_pricing não encontrado para substituição")

facade_path.write_text(facade, encoding="utf-8")
print(f"Arquivo atualizado: {facade_path}")

# ------------------------------------------------------------------
# Patch 5: UI não deve mascarar erro de recálculo
# ------------------------------------------------------------------
old_ui = "                facade.execute_pricing(sid)\n"

new_ui = '''                result = facade.execute_pricing(sid)

                if isinstance(result, dict) and result.get("status") == "error":
                    raise RuntimeError(
                        result.get("error_message") or "Erro no recálculo automático"
                    )
'''

if old_ui in ui:
    ui = ui.replace(old_ui, new_ui, 1)
    ui_path.write_text(ui, encoding="utf-8")
    print(f"UI atualizada: {ui_path}")
else:
    if "Erro no recálculo automático" in ui:
        print("UI aparentemente já valida status=error")
    else:
        raise SystemExit("Trecho facade.execute_pricing(sid) não encontrado na UI")

# ------------------------------------------------------------------
# Patch 6: teste de regressão
# ------------------------------------------------------------------
test_code = '''from pathlib import Path

import services.canonical_pricing_facade as facade_module


class FakePricingInputService:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        return {
            "structure_id": structure_id,
            "structure_name": "Estrutura Manual",
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
            "pricing_payload": pricing_payload,
            "result": {
                "engine": "fake",
                "status": "ok",
                "metrics": {
                    "number_of_legs": 0,
                    "total_quantity": 0,
                },
                "valuation": {
                    "theoretical_value": 0,
                },
            },
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
            "record": {
                "id": 1,
                "structure_id": pricing_payload["structure_id"],
                "execution_status": result.get("status"),
            }
        }


def test_facade_falls_back_to_canonical_manual_payload_when_alias_is_null(monkeypatch, tmp_path):
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
        structure_id=123,
        reference_date="2026-06-21",
    )

    assert response["status"] == "ok"
    assert response["pricing_payload"]["structure_id"] == 123
    assert response["pricing_payload"]["reference_date"] == "2026-06-21"
    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
    assert response["pricing_payload"]["meta"]["alias_legacy_aba"] is None
    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]

    assert len(persister.calls) == 1
    assert persister.calls[0]["pricing_payload"]["structure_id"] == 123
    assert persister.calls[0]["result"]["status"] == "ok"
'''

test_path.parent.mkdir(parents=True, exist_ok=True)
test_path.write_text(test_code, encoding="utf-8")
print(f"Teste criado/atualizado: {test_path}")

print()
print("Patches concluídos.")
PY

echo >> "$OUT"
echo "3) Diff apos patch" >> "$OUT"
git diff -- services/canonical_pricing_facade.py UI/main_window.py ATT/tests/test_canonical_pricing_facade_manual_without_alias.py >> "$OUT" 2>&1 || true
echo >> "$OUT"

echo "4) Compilacao Python" >> "$OUT"
python -m py_compile \
  services/canonical_pricing_facade.py \
  UI/main_window.py \
  ATT/tests/test_canonical_pricing_facade_manual_without_alias.py >> "$OUT" 2>&1
echo "py_compile OK" >> "$OUT"
echo >> "$OUT"

echo "5) Teste de regressao novo" >> "$OUT"
python -m pytest -q ATT/tests/test_canonical_pricing_facade_manual_without_alias.py >> "$OUT" 2>&1
echo >> "$OUT"

echo "6) Testes focados disponiveis" >> "$OUT"

TESTS=()
for t in \
  "ATT/tests/test_pricing_input_service.py" \
  "ATT/tests/test_pricing_execution_persistence_service.py" \
  "ATT/tests/test_structure_editor_integration.py" \
  "ATT/tests/test_derived_service.py"
do
  if [ -f "$t" ]; then
    TESTS+=("$t")
  fi
done

if [ "${#TESTS[@]}" -gt 0 ]; then
  python -m pytest -q "${TESTS[@]}" >> "$OUT" 2>&1
else
  echo "Nenhum teste focado adicional encontrado." >> "$OUT"
fi

echo >> "$OUT"
echo "7) Status final git" >> "$OUT"
git status --short >> "$OUT" 2>&1 || true

echo >> "$OUT"
echo "== Fim Fase 3E fix ==" >> "$OUT"

echo "$OUT"
tail -220 "$OUT"
