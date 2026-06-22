from pathlib import Path

path = Path("services/derived_payoff_persistence.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(".py.bak-fase-3f-fix1")
backup.write_text(text, encoding="utf-8")

helper = r'''
    @staticmethod
    def _normalize_position_side(value: Any, quantity: Any = None) -> str | None:
        """
        Normaliza aliases de direção para o contrato canônico de payoff.

        domain/payoff.py exige leg["position_side"].
        Payloads vindos da UI/manual podem vir com leg["side"].
        """
        raw = "" if value is None else str(value).strip().upper()

        aliases = {
            "BUY": "LONG",
            "BOUGHT": "LONG",
            "COMPRA": "LONG",
            "COMPRADO": "LONG",
            "LONG": "LONG",
            "SELL": "SHORT",
            "SOLD": "SHORT",
            "VENDA": "SHORT",
            "VENDIDO": "SHORT",
            "SHORT": "SHORT",
        }

        if raw in aliases:
            return aliases[raw]

        try:
            q = float(quantity)
            if q < 0:
                return "SHORT"
            if q > 0:
                return "LONG"
        except (TypeError, ValueError):
            pass

        return None

    @staticmethod
    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
        """
        Adapta uma leg recebida de fontes legadas/manuais para o contrato
        esperado por domain.compute_payoff_from_canonical_input().

        Correção principal da Fase 3F Fix1:
          side -> position_side

        Também mantém aliases úteis sem remover os campos originais.
        """
        data = dict(leg) if isinstance(leg, dict) else dict(vars(leg))

        quantity = data.get("quantity", data.get("quant"))
        position_side = data.get("position_side") or data.get("side")

        normalized_side = DerivedPayoffPersistence._normalize_position_side(
            position_side,
            quantity,
        )

        if normalized_side:
            data["position_side"] = normalized_side
            data.setdefault("side", normalized_side)

        if quantity is not None:
            try:
                # No contrato canônico, a direção fica em position_side.
                # A quantidade deve ser magnitude positiva.
                data["quantity"] = abs(float(quantity))
            except (TypeError, ValueError):
                data["quantity"] = quantity

        option_type = data.get("option_type")
        if option_type is not None:
            data["option_type"] = str(option_type).strip().upper()

        instrument_type = data.get("instrument_type")
        if instrument_type is not None:
            data["instrument_type"] = str(instrument_type).strip().upper()

        # Aliases defensivos para eventuais payloads de outras origens.
        if "premium" not in data and "price" in data:
            data["premium"] = data.get("price")

        if "price" not in data and "premium" in data:
            data["price"] = data.get("premium")

        if "symbol" not in data:
            data["symbol"] = data.get("asset") or data.get("ativo")

        return data

    @staticmethod
    def _normalize_canonical_input_for_payoff(
        canonical_input: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
        """
        normalized = dict(canonical_input)

        structure = dict(normalized.get("structure") or {})
        market = dict(normalized.get("market") or {})
        meta = dict(normalized.get("meta") or {})

        legs = structure.get("legs") or []
        structure["legs"] = [
            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
            for leg in legs
        ]

        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")

        normalized["structure"] = structure
        normalized["market"] = market
        normalized["meta"] = meta

        return normalized

'''

marker = '''    @staticmethod
    def _build_canonical_input(
'''

if helper.strip() not in text:
    if marker not in text:
        raise SystemExit("Marcador de _build_canonical_input não encontrado.")
    text = text.replace(marker, helper + "\n" + marker)

old_a = '''        # Formato A -- já canônico
        if "structure" in pricing_payload and "market" in pricing_payload:
            return pricing_payload
'''

new_a = '''        # Formato A -- já canônico, mas ainda assim normalizado para o contrato
        # estrito de domain/payoff.py.
        if "structure" in pricing_payload and "market" in pricing_payload:
            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
                pricing_payload
            )
'''

if old_a not in text:
    raise SystemExit("Bloco Formato A não encontrado para substituição.")

text = text.replace(old_a, new_a)

old_b = '''        legs           = pricing_payload.get("legs") or []

        return {
            "structure": {
                "structure_id":    structure_id,
                "name":            structure_name,
                "underlying_asset": underlying,
                "legs":            legs,
            },
            "market": {
                "spot_price":       spot_price,
                "underlying_asset": underlying,
                "reference_date":   reference_date,
            },
            "meta": {
                "source": "pricing_execution_persistence",
            },
        }
'''

new_b = '''        legs           = pricing_payload.get("legs") or []

        payload_meta = pricing_payload.get("meta")
        meta = dict(payload_meta) if isinstance(payload_meta, dict) else {}
        meta.setdefault("source", "pricing_execution_persistence")
        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")

        canonical_input = {
            "structure": {
                "structure_id":    structure_id,
                "name":            structure_name,
                "underlying_asset": underlying,
                "legs": [
                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
                    for leg in legs
                ],
            },
            "market": {
                "spot_price":       spot_price,
                "underlying_asset": underlying,
                "reference_date":   reference_date,
            },
            "meta": meta,
        }

        return canonical_input
'''

if old_b not in text:
    raise SystemExit("Bloco Formato B não encontrado para substituição.")

text = text.replace(old_b, new_b)

path.write_text(text, encoding="utf-8")

print("Patch aplicado em:", path)
print("Backup criado em:", backup)
