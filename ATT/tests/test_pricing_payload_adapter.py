import unittest

from services.pricing_payload_adapter import to_pricing_payload


class PricingPayloadAdapterTests(unittest.TestCase):
    def test_should_not_include_alias_legacy_aba_in_pricing_payload(self):
        canonical_input = {
            "structure": {
                "structure_id": 7,
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
            },
            "market": {
                "reference_date": "2026-05-18",
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            },
        }

        payload = to_pricing_payload(canonical_input)

        self.assertEqual(payload["structure_id"], 7)
        self.assertEqual(payload["underlying_asset"], "BOVA11")
        self.assertNotIn("alias_legacy_aba", payload)

    def test_should_map_legs_to_pricing_shape(self):
        canonical_input = {
            "structure": {
                "structure_id": 7,
                "name": "BOVA11 Condor Maio/2026",
                "underlying_asset": "BOVA11",
                "legs": [
                    {
                        "position_side": "short",
                        "option_type": "put",
                        "symbol": "bovaq195",
                        "strike": 195,
                        "expiration_date": "2026-05-15",
                        "quantity": 4000,
                        "premium": 1.25,
                        "multiplier": 1,
                    }
                ],
            },
            "market": {
                "reference_date": "2026-05-18",
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            },
        }

        payload = to_pricing_payload(canonical_input)

        self.assertEqual(len(payload["legs"]), 1)
        self.assertEqual(payload["legs"][0]["side"], "SHORT")
        self.assertEqual(payload["legs"][0]["option_type"], "PUT")
        self.assertEqual(payload["legs"][0]["symbol"], "BOVAQ195")
        self.assertEqual(payload["legs"][0]["instrument_type"], "OPTION")


if __name__ == "__main__":
    unittest.main()
