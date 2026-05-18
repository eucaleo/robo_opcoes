import unittest
from datetime import datetime

from services.robo_leg_mapper import to_canonical_leg


class RoboLegMapperTests(unittest.TestCase):
    def test_should_map_call_buy_leg_to_canonical(self):
        leg = {
            "cv": "C",
            "call_put": "CALL",
            "ativo": "bovae195",
            "strike": 195,
            "vencimento": datetime(2026, 5, 15),
            "quant": 5000,
            "preco": 1.25,
        }

        result = to_canonical_leg(leg)

        self.assertEqual(result["position_side"], "LONG")
        self.assertEqual(result["option_type"], "CALL")
        self.assertEqual(result["symbol"], "BOVAE195")
        self.assertEqual(result["strike"], 195.0)
        self.assertEqual(result["expiration_date"], "2026-05-15")
        self.assertEqual(result["quantity"], 5000)
        self.assertEqual(result["premium"], 1.25)
        self.assertEqual(result["multiplier"], 1.0)

    def test_should_map_put_sell_leg_to_canonical(self):
        leg = {
            "cv": "V",
            "call_put": "PUT",
            "ativo": "bovaq180",
            "strike": "180",
            "vencimento": datetime(2026, 6, 19),
            "quant": "3000",
            "preco": "2.5",
        }

        result = to_canonical_leg(leg, multiplier=100)

        self.assertEqual(result["position_side"], "SHORT")
        self.assertEqual(result["option_type"], "PUT")
        self.assertEqual(result["symbol"], "BOVAQ180")
        self.assertEqual(result["strike"], 180.0)
        self.assertEqual(result["expiration_date"], "2026-06-19")
        self.assertEqual(result["quantity"], 3000)
        self.assertEqual(result["premium"], 2.5)
        self.assertEqual(result["multiplier"], 100.0)

    def test_should_accept_object_attributes(self):
        class FakeLeg:
            cv = "C"
            call_put = "PUT"
            ativo = "bovaq170"
            strike = 170
            vencimento = datetime(2026, 7, 17)
            quant = 2000
            preco = None

        result = to_canonical_leg(FakeLeg())

        self.assertEqual(result["position_side"], "LONG")
        self.assertEqual(result["option_type"], "PUT")
        self.assertEqual(result["symbol"], "BOVAQ170")
        self.assertEqual(result["strike"], 170.0)
        self.assertEqual(result["expiration_date"], "2026-07-17")
        self.assertEqual(result["quantity"], 2000)
        self.assertIsNone(result["premium"])
        self.assertEqual(result["multiplier"], 1.0)

    def test_should_raise_when_cv_is_invalid(self):
        leg = {
            "cv": "X",
            "call_put": "CALL",
            "ativo": "bovae195",
            "strike": 195,
            "vencimento": datetime(2026, 5, 15),
            "quant": 5000,
            "preco": 1.25,
        }

        with self.assertRaises(ValueError) as ctx:
            to_canonical_leg(leg)

        self.assertIn("invalid cv", str(ctx.exception))

    def test_should_raise_when_call_put_is_invalid(self):
        leg = {
            "cv": "C",
            "call_put": "XXX",
            "ativo": "bovae195",
            "strike": 195,
            "vencimento": datetime(2026, 5, 15),
            "quant": 5000,
            "preco": 1.25,
        }

        with self.assertRaises(ValueError) as ctx:
            to_canonical_leg(leg)

        self.assertIn("invalid call_put", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
