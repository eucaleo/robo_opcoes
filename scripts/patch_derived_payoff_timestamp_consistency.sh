#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from pathlib import Path
from datetime import datetime

path = Path("services/derived_payoff_persistence.py")

if not path.exists():
    raise SystemExit("[ERROR] Arquivo não encontrado: services/derived_payoff_persistence.py")

text = path.read_text(encoding="utf-8")
original = text

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = path.with_suffix(path.suffix + f".bak-{stamp}")
backup.write_text(text, encoding="utf-8")
print(f"[INFO] Backup criado: {backup}")

def replace_required(src: str, old: str, new: str, label: str) -> str:
    if old not in src:
        raise SystemExit(f"[ERROR] Trecho não encontrado para patch: {label}")
    return src.replace(old, new, 1)

# ---------------------------------------------------------------------
# Import datetime/timezone
# ---------------------------------------------------------------------
if "from datetime import datetime, timezone" not in text:
    text = replace_required(
        text,
        "import logging\n",
        "import logging\nfrom datetime import datetime, timezone\n",
        "import datetime/timezone",
    )

# ---------------------------------------------------------------------
# persist(): criar timestamp único e só gravar decisão se payoff gravou
# ---------------------------------------------------------------------
if "snapshot_ts = datetime.now(timezone.utc).isoformat()" not in text:
    text = replace_required(
        text,
        """        self._persist_payoff(pricing_payload, result)
        self._persist_decision(pricing_payload, result)
""",
        """        # Timestamp único para payoff + decisão.
        # Evita snapshots inconsistentes por diferença de milissegundos entre gravações.
        snapshot_ts = datetime.now(timezone.utc).isoformat()

        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
        if not payoff_saved:
            logger.warning(
                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return

        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
        if not decision_saved:
            logger.error(
                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
                pricing_payload.get("structure_id"),
                snapshot_ts,
            )
""",
        "persist timestamp único",
    )

# ---------------------------------------------------------------------
# _persist_payoff signature: retorna bool e recebe snapshot_ts
# ---------------------------------------------------------------------
if "snapshot_ts: str,\n    ) -> bool:" not in text:
    text = replace_required(
        text,
        """    def _persist_payoff(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
""",
        """    def _persist_payoff(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
        snapshot_ts: str,
    ) -> bool:
""",
        "_persist_payoff signature",
    )

# payoff sem pontos deve retornar False
text = text.replace(
    """            if not payoff_result.get("points"):
                logger.warning(
                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
                    pricing_payload.get("structure_id"),
                )
                return
""",
    """            if not payoff_result.get("points"):
                logger.warning(
                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
                    pricing_payload.get("structure_id"),
                )
                return False
""",
    1,
)

# salvar payoff com timestamp único
text = text.replace(
    "            save_payoff_from_canonical_payload(payoff_result)\n",
    "            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)\n",
    1,
)

# payoff sucesso retorna True
if 'derived_payoff_persistence: %d pontos gravados -- structure_id=%s' in text and "return True\n\n        except Exception:" not in text:
    text = replace_required(
        text,
        """            logger.info(
                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
                len(payoff_result["points"]),
                pricing_payload.get("structure_id"),
            )

        except Exception:
""",
        """            logger.info(
                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
                len(payoff_result["points"]),
                pricing_payload.get("structure_id"),
            )
            return True

        except Exception:
""",
        "_persist_payoff return True",
    )

# payoff exception retorna False
if "erro ao gravar payoff" in text and "return False\n\n    # -------------------------------------------------------------- #\n    #  decisão" not in text:
    text = replace_required(
        text,
        """            logger.exception(
                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

    # -------------------------------------------------------------- #
    #  decisão""",
        """            logger.exception(
                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return False

    # -------------------------------------------------------------- #
    #  decisão""",
        "_persist_payoff return False exception",
    )

# ---------------------------------------------------------------------
# _persist_decision signature: retorna bool e recebe snapshot_ts
# ---------------------------------------------------------------------
if "snapshot_ts: str,\n    ) -> bool:" in text:
    # cuidado: já pode existir no payoff; testar assinatura específica da decisão
    pass

if """    def _persist_decision(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
""" in text:
    text = replace_required(
        text,
        """    def _persist_decision(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
""",
        """    def _persist_decision(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
        snapshot_ts: str,
    ) -> bool:
""",
        "_persist_decision signature",
    )

# salvar decisão com timestamp único
if "timestamp=snapshot_ts," not in text:
    text = replace_required(
        text,
        """                structure_name=pricing_payload.get("structure_name"),
                underlying_asset=pricing_payload.get("underlying_asset"),
            )
""",
        """                structure_name=pricing_payload.get("structure_name"),
                underlying_asset=pricing_payload.get("underlying_asset"),
                timestamp=snapshot_ts,
            )
""",
        "save_decision timestamp",
    )

# decisão sucesso retorna True
if 'derived_payoff_persistence: decisão gravada -- structure_id=%s' in text and "return True\n\n        except Exception:" in text:
    # Já existe return True em payoff; precisamos garantir decisão também.
    pass

decision_success_old = """            logger.info(
                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

        except Exception:
"""

decision_success_new = """            logger.info(
                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return True

        except Exception:
"""

# Troca a ocorrência da decisão se ainda não tiver return True nesse bloco
if decision_success_old in text:
    text = text.replace(decision_success_old, decision_success_new, 1)

# decisão exception retorna False
decision_exception_old = """            logger.exception(
                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

    # -------------------------------------------------------------- #
    #  helpers"""

decision_exception_new = """            logger.exception(
                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return False

    # -------------------------------------------------------------- #
    #  helpers"""

if decision_exception_old in text:
    text = text.replace(decision_exception_old, decision_exception_new, 1)

# ---------------------------------------------------------------------
# Validações mínimas do patch
# ---------------------------------------------------------------------
required = [
    "from datetime import datetime, timezone",
    "snapshot_ts = datetime.now(timezone.utc).isoformat()",
    "save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)",
    "timestamp=snapshot_ts,",
    "payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)",
    "decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)",
]

missing = [item for item in required if item not in text]
if missing:
    print("[ERROR] Patch incompleto. Itens ausentes:")
    for item in missing:
        print(f"  - {item}")
    raise SystemExit(1)

if text == original:
    print("[INFO] Nenhuma alteração aplicada; arquivo possivelmente já estava corrigido.")
else:
    path.write_text(text, encoding="utf-8")
    print("[OK] Patch aplicado em services/derived_payoff_persistence.py")
PY

python -m py_compile services/derived_payoff_persistence.py
echo "[OK] py_compile passou."
