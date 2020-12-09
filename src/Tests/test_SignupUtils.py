from unittest import TestCase
from ..Utils.SignupUtils import SignupUtils
import asyncio


class TestSignupUtils(TestCase):
    def test_check_duplicate_true_damage(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": ["Test"], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    def test_check_duplicate_true_healer(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": ["Test"], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    def test_check_duplicate_true_tank(self):
        ops = {"Sign-ups": {"Tank": ["Test"], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    def test_check_duplicate_true_reserve(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": ["Test"],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    # def test_check_role_change(self):
    #     self.fail()
