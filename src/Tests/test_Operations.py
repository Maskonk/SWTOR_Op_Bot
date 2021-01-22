from unittest import TestCase
import asyncio
from src.Cogs.Operations import Operations
from copy import deepcopy


class TestOperations(TestCase):
    def test_add_signup_Tank_no_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Tank", None))
        loop.close()
        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Tank", "alt-role": None}]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Dps_no_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Dps", None))
        loop.close()
        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Dps", "alt-role": None}]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Heal_no_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Healer", None))
        loop.close()
        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Healer", "alt-role": None}]
        ops["Signed"] = 1
        self.assertEqual(ops, result)

    def test_add_signup_Tank_with_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Tank", "Dps"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Tank", "alt-role": "Dps"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_signup_Dps_with_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Dps", "Healer"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Dps", "alt-role": "Healer"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_signup_Healer_with_alt(self):
        ops = {"Sign-ups": {"Roster": [], "Reserves": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_signup(ops2, "Test", "Healer", "Tank"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Healer", "alt-role": "Tank"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_any_signup_default_to_Dps(self):
        ops = {"Size": ("8", {"Dps": 1}), "Sign-ups": {"Roster": []}, "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_any_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Dps", "alt-role": "Any"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_any_signup_switches_to_Healer(self):
        ops = {"Size": ("8", {"Dps": 4, "Healer": 1}),
               "Sign-ups": {"Roster": [{"name": "Test1", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test2", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test3", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test4", "main-role": "Dps", "alt-role": "Any"}]},
               "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_any_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Healer", "alt-role": "Any"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_any_signup_finally_tries_Tank(self):
        ops = {"Size": ("8", {"Dps": 4, "Healer": 2, "Tank": 1}),
               "Sign-ups": {"Roster": [{"name": "Test1", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test2", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test3", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test4", "main-role": "Dps", "alt-role": "Any"},
                                                    {"name": "Test5", "main-role": "Healer", "alt-role": "Any"},
                                                    {"name": "Test6", "main-role": "Healer", "alt-role": "Any"}]},
               "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_any_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"] += [{"name": "Test", "main-role": "Tank", "alt-role": "Any"}]
        ops["Signed"] = 1
        self.assertDictEqual(ops, result)

    def test_add_reserve(self):
        ops = {"Size": "8", "Sign-ups": {"Reserves": []},
               "Signed": 0}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.add_reserve(ops2, "Test", "Tank"))
        loop.close()

        ops["Sign-ups"]["Reserves"] += [{"name": "Test", "role": "Tank", "move-main": False}]
        self.assertDictEqual(ops, result)

    def test_remove_signup_one_role_Tank(self):
        ops = {"Size": "8", "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Tank", "alt-role": None}],
                                         "Reserves": []},
               "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.remove_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"].remove({"name": "Test", "main-role": "Tank", "alt-role": None})
        ops["Signed"] = 0
        self.assertDictEqual(ops, result)

    def test_remove_signup_one_role_Dps(self):
        ops = {"Size": "8", "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Dps", "alt-role": None}],
                                         "Reserves": []},
               "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.remove_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"].remove({"name": "Test", "main-role": "Dps", "alt-role": None})
        ops["Signed"] = 0
        self.assertDictEqual(ops, result)

    def test_remove_signup_one_role_Healer(self):
        ops = {"Size": "8", "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Healer", "alt-role": None}],
                                         "Reserves": []},
               "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.remove_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"].remove({"name": "Test", "main-role": "Healer", "alt-role": None})
        ops["Signed"] = 0
        self.assertDictEqual(ops, result)

    def test_remove_signup_two_roles(self):
        ops = {"Size": "8", "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Dps", "alt-role": "Tank"}],
                                         "Reserves": []},
               "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.remove_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Roster"].remove({"name": "Test", "main-role": "Dps", "alt-role": "Tank"})
        ops["Signed"] = 0
        self.assertDictEqual(ops, result)

    def test_remove_signup_reserve(self):
        ops = {"Size": "8", "Sign-ups": {"Roster": [],
                                         "Reserves": [{"name": "Test", "role": "Dps", "move-main": False}]},
               "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.remove_signup(ops2, "Test"))
        loop.close()

        ops["Sign-ups"]["Reserves"].remove({"name": "Test", "role": "Dps", "move-main": False})
        ops["Signed"] = 0
        self.assertDictEqual(ops, result)

    def test_check_role_full_Tank_false(self):
        ops = {"Size": ("8", {"Tank": 2}),
               "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Tank", "alt-role": None}],
                                         "Reserves": []}, "Signed": 1}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.check_role_full(ops2, "Tank"))
        loop.close()

        self.assertFalse(result)

    def test_check_role_full_Tank_true(self):
        ops = {"Size": ("8", {"Tank": 2}),
               "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Tank", "alt-role": None},
                                                    {"name": "Test", "main-role": "Tank", "alt-role": "Dps"}],
                                         "Reserves": []}, "Signed": 2}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.check_role_full(ops2, "Tank"))
        loop.close()

        self.assertTrue(result)

    def test_check_role_full_Healer_true(self):
        ops = {"Size": ("8", {"Healer": 2}) ,
               "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Healer", "alt-role": None},
                                                   {"name": "Test", "main-role": "Healer", "alt-role": "Dps"}],
                                        "Reserves": []}, "Signed": 2}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.check_role_full(ops2, "Healer"))
        loop.close()

        self.assertTrue(result)

    def test_check_role_full_Dps_true(self):
        ops = {"Size": ("8", {"Dps": 4}),
               "Sign-ups": {"Roster": [{"name": "Test", "main-role": "Dps", "alt-role": None},
                                                   {"name": "Test", "main-role": "Dps", "alt-role": "Dps"},
                                                   {"name": "Test", "main-role": "Dps", "alt-role": "Dps"},
                                                   {"name": "Test", "main-role": "Dps", "alt-role": "Dps"}],
                                        "Reserves": []}, "Signed": 4}
        ops2 = deepcopy(ops)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(Operations.check_role_full(ops2, "Dps"))
        loop.close()

        self.assertTrue(result)


    # def test_parse_date(self):
    #     self.fail()
    #
    # def test_date_extension(self):
    #     self.fail()
    #
    # def test_add_to_operation(self):
    #     self.fail()
