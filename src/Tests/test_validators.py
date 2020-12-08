from unittest import TestCase
from ..Utils.Validators import Validators
import asyncio
from dateutil.parser._parser import ParserError
from datetime import datetime


class TestValidators(TestCase):
    def setUp(self) -> None:
        pass

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
        result = loop.run_until_complete(Validators.validate_role("t"))
        loop.close()
        self.assertEqual("Tank", result)

    def test_validate_role_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_role("x"))
        loop.close()
        self.assertEqual("", result)

    def test_validate_side_input_valid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_side_input("rep"))
        loop.close()
        self.assertEqual("Rep", result)

    def test_validate_side_input_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_side_input("blue"))
        loop.close()
        self.assertEqual(None, result)

    def test_validate_size_input_valid(self):
        sizes = {"1": {"Tank": 0, "Dps": 1, "Healer": 0}, "4": {"Tank": 1, "Dps": 1, "Healer": 1},
                 "8": {"Tank": 2, "Dps": 4, "Healer": 2}, "16": {"Tank": 2, "Dps": 10, "Healer": 4},
                 "1t5d": {"Tank": 1, "Dps": 5, "Healer": 2}, "1h5d": {"Tank": 2, "Dps": 5, "Healer": 1},
                 "6d": {"Tank": 1, "Dps": 6, "Healer": 1}, "24": {"Tank": 3, "Dps": 15, "Healer": 6}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_size_input("1t5d", sizes))
        loop.close()
        self.assertTrue(result)

    def test_validate_size_input_invalid(self):
        sizes = {"1": {"Tank": 0, "Dps": 1, "Healer": 0}, "4": {"Tank": 1, "Dps": 1, "Healer": 1},
                 "8": {"Tank": 2, "Dps": 4, "Healer": 2}, "16": {"Tank": 2, "Dps": 10, "Healer": 4},
                 "1t5d": {"Tank": 1, "Dps": 5, "Healer": 2}, "1h5d": {"Tank": 2, "Dps": 5, "Healer": 1},
                 "6d": {"Tank": 1, "Dps": 6, "Healer": 1}, "24": {"Tank": 3, "Dps": 15, "Healer": 6}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Validators.validate_size_input("22", sizes))
        loop.close()
        self.assertFalse(result)

    # def test_validate_operation_input(self):
    #     self.fail()
    #
    # def test_validate_operation_channel(self):
    #     self.fail()
    #
    # def test_validate_sign_up_channel(self):
    #     self.fail()
    #
    # def test_validate_swtor_channel(self):
    #     self.fail()
