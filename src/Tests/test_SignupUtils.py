from unittest import TestCase
from src.Utils.SignupUtils import SignupUtils
import asyncio


class TestSignupUtils(TestCase):
    def test_check_duplicate_true(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Test"}]}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    def test_check_duplicate_true_reserve(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": [{"name": "Test"}]}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertTrue(result)

    def test_check_duplicate_false(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Bob"}], "Reserves": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_duplicate(ops, "Test"))
        loop.close()
        self.assertFalse(result)

    def test_check_role_change_main_role_no_alt_role(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Test", "main-role": "Healer", "alt-role": None}], "Reserves": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Tank", None))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_alt_role_no_main_change(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Test", "main-role": "Healer", "alt-role": "Dps"}], "Reserves": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Healer", "Tank"))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_both_roles_change(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Test", "main-role": "Dps", "alt-role": "Tank"}], "Reserves": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Tank", "Dps"))
        loop.close()
        self.assertTrue(result)

    def test_check_role_change_no_change(self):
        ops = {"Sign-ups": {"Roster": [{"name": "Test", "main-role": "Healer", "alt-role": "Dps"}], "Reserves": []}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(SignupUtils.check_role_change(ops, "Test", "Healer", "Dps"))
        loop.close()
        self.assertFalse(result)
