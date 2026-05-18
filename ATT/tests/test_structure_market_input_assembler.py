import unittest

from services.structure_market_input_assembler import assemble_structure_market_input


class StructureMarketInputAssemblerTests(unittest.TestCase):
    def test_should_assemble_structure_and_market_input(self):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "CALL",
                    "symbol": "BOVAE195",
                    "strike": 195.0,
                    "expiration_date": "2026-05-15",
                    "quantity": 5000,
                    "premium": None,
                    "multiplier": 1.0,
                }
            ],
        }

        market_snapshot = {
            "reference_date": "2026-05-18",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        }

        result = assemble_structure_market_input(structure, market_snapshot)

        self.assertIn("structure", result)
        self.assertIn("market", result)
        self.assertIn("meta", result)

        self.assertEqual(result["structure"]["underlying_asset"], "BOVA11")
        self.assertEqual(result["market"]["underlying_asset"], "BOVA11")
        self.assertEqual(result["market"]["reference_date"], "2026-05-18")
        self.assertEqual(result["meta"]["input_source"], "structure_market_input_assembler")

    def test_should_raise_when_underlying_asset_mismatches(self):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "legs": [],
        }

        market_snapshot = {
            "reference_date": "2026-05-18",
            "underlying_asset": "PETR4",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        }

        with self.assertRaises(ValueError) as ctx:
            assemble_structure_market_input(structure, market_snapshot)

        self.assertIn("underlying_asset mismatch", str(ctx.exception))

    def test_should_raise_when_structure_is_missing(self):
        market_snapshot = {
            "reference_date": "2026-05-18",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        }

        with self.assertRaises(ValueError) as ctx:
            assemble_structure_market_input({}, market_snapshot)

        self.assertIn("structure is required", str(ctx.exception))

    def test_should_raise_when_market_snapshot_is_missing(self):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "legs": [],
        }

        with self.assertRaises(ValueError) as ctx:
            assemble_structure_market_input(structure, {})

        self.assertIn("market_snapshot is required", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
