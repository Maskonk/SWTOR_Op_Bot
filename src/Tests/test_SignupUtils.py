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

    def test_check_duplicate_false(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertFalse(result)

    def test_check_role_change_main_role_no_alt_role(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": ["Test"], "Reserve": ["Test"],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Tank", ""))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_alt_role_no_main_change(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": ["Test"], "Reserve": ["Test"],
                            "Alternate_Tank": [], "Alternate_Dps": ["Test"], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Healer", "Tank"))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_both_roles_change(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": ["Test"], "Reserve": ["Test"],
                            "Alternate_Tank": [], "Alternate_Dps": ["Test"], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Tank", "Tank"))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_no_change(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": ["Test"], "Reserve": ["Test"],
                            "Alternate_Tank": [], "Alternate_Dps": ["Test"], "Alternate_Healer": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Healer", "Dps"))
        loop.close()
        self.assertFalse(result)
