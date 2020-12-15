from unittest import TestCase
import asyncio
from ..Cogs.Operations import Operations
from copy import deepcopy


class TestOperations(TestCase):
    def test_add_signup_Tank_no_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Tank", None))
        loop.close()
        ops["Sign-ups"]["Tank"] += ["Test"]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Dps_no_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Dps", None))
        loop.close()
        ops["Sign-ups"]["Dps"] += ["Test"]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Heal_no_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Healer", None))
        loop.close()
        ops["Sign-ups"]["Healer"] += ["Test"]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Tank_with_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Tank", "Dps"))
        loop.close()

        ops["Sign-ups"]["Tank"] += ["Test (Dps)"]
        ops["Sign-ups"]["Alternate_Dps"] += ["Test"]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_signup_Dps_with_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Dps", "Healer"))
        loop.close()

        ops["Sign-ups"]["Dps"] += ["Test (Healer)"]
        ops["Sign-ups"]["Alternate_Healer"] += ["Test"]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_signup_Healer_with_alt(self):
        ops = {"Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Healer", "Tank"))
        loop.close()

        ops["Sign-ups"]["Healer"] += ["Test (Tank)"]
        ops["Sign-ups"]["Alternate_Tank"] += ["Test"]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_any_signup_default_to_dps(self):
        ops = {"Size": "8", "Sign-ups": {"Tank": [], "Dps": [], "Healer": [], "Reserve": [],
                            "Alternate_Tank": [], "Alternate_Dps": [], "Alternate_Healer": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_any_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Dps"] += ["Test (Any)"]
        ops["Sign-ups"]["Alternate_Tank"] += ["Test"]
        ops["Sign-ups"]["Alternate_Healer"] += ["Test"]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    # def test_add_reserve(self):
    #     self.fail()
    #
    # def test_remove_signup(self):
    #     self.fail()
    #
    # def test_is_owner_or_admin(self):
    #     self.fail()
    #
    # def test_parse_date(self):
    #     self.fail()
    #
    # def test_date_extension(self):
    #     self.fail()
    #
    # def test_check_role_full(self):
    #     self.fail()
    #
    # def test_add_to_operation(self):
    #     self.fail()
