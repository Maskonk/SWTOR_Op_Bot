from unittest import TestCase
from src.Utils.Validators import Validators
import asyncio
from dateutil.parser._parser import ParserError
from datetime import datetime


class TestValidators(TestCase):
    sizes = {"1": {"Tank": 0, "Dps": 1, "Healer": 0}, "4": {"Tank": 1, "Dps": 1, "Healer": 1},
             "8": {"Tank": 2, "Dps": 4, "Healer": 2}, "16": {"Tank": 2, "Dps": 10, "Healer": 4},
             "1t5d": {"Tank": 1, "Dps": 5, "Healer": 2}, "1h5d": {"Tank": 2, "Dps": 5, "Healer": 1},
             "6d": {"Tank": 1, "Dps": 6, "Healer": 1}, "24": {"Tank": 3, "Dps": 15, "Healer": 6}}

    operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                  "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                  "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                  "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                  "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eyeless": "Eyeless",
                  "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}

    def test_validate_time_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_time_input("11/12/2021", "11:20"))
        loop.close()
        self.assertTrue(result)

    def test_validate_time_input_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_time_input("11/12/19", "11:20"))
        loop.close()
        self.assertFalse(result)

    def test_validate_time_input_bad_format(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_time_input("Blueberry", "11:20"))
        loop.close()
        self.assertFalse(result)

    def test_validate_difficulty_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_difficulty_input("SM"))
        loop.close()
        self.assertTrue(result)

    def test_validate_difficulty_input_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_difficulty_input("RM"))
        loop.close()
        self.assertFalse(result)

    def test_validate_role_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_role("dwt"))
        loop.close()
        self.assertEqual("Dwt", result)

    def test_validate_role_invalid(self):
        loop = asyncio.new_event_loop()
        with self.assertRaises(Exception) as context:
            loop.run_until_complete(Validators.validate_role("blue"))
        loop.close()
        self.assertTrue("Invalid role." in str(context.exception))

    def test_validate_side_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_side_input("rep"))
        loop.close()
        self.assertEqual("Rep", result)

    def test_validate_side_input_invalid(self):
        loop = asyncio.new_event_loop()
        with self.assertRaises(Exception) as context:
            loop.run_until_complete(Validators.validate_side_input("blue"))
        loop.close()
        self.assertTrue("Invalid side." in str(context.exception))

    def test_validate_size_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_size_input("1t5d", self.sizes))
        loop.close()
        self.assertTrue(result)

    def test_validate_size_input_invalid(self):
        loop = asyncio.new_event_loop()
        with self.assertRaises(Exception) as context:
            loop.run_until_complete(Validators.validate_size_input("blue", {"Dps": 4}))
        loop.close()
        self.assertTrue("No valid role sizes found. There must be at least one valid role." in str(context.exception))

    def test_validate_operation_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_operation_input("dp", self.operations))
        loop.close()
        self.assertTrue(result)

    def test_validate_operation_input_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_operation_input("vp", self.operations))
        loop.close()
        self.assertFalse(result)

    def test_validate_operation_channel_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_operation_channel(12345, {"Operation_channels": [12345]}))
        loop.close()
        self.assertTrue(result)

    def test_validate_operation_channel_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_operation_channel(12345, {"Operation_channels": [67890]}))
        loop.close()
        self.assertFalse(result)

    def test_validate_operation_channel_none(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_operation_channel(12345, {}))
        loop.close()
        self.assertTrue(result)

    def test_validate_sign_up_channel_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_sign_up_channel(12345, {"Signup_channels": [12345]}))
        loop.close()
        self.assertTrue(result)

    def test_validate_sign_up_channel_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_sign_up_channel(12345, {"Signup_channels": [67890]}))
        loop.close()
        self.assertFalse(result)

    def test_validate_sign_up_channel_none(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_sign_up_channel(12345, {}))
        loop.close()
        self.assertTrue(result)

    def test_validate_swtor_channel_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_swtor_channel(12345, {"Fun_channels": [12345]}))
        loop.close()
        self.assertTrue(result)

    def test_validate_swtor_channel_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_swtor_channel(12345, {"Fun_channels": [67890]}))
        loop.close()
        self.assertFalse(result)

    def test_validate_swtor_channel_none(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_swtor_channel(12345, {}))
        loop.close()
        self.assertTrue(result)
