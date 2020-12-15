from unittest import TestCase
import asyncio
from src.Utils.ReactionUtils import check_valid_reaction


class Test(TestCase):
    def test_check_valid_reaction_tank(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Tank"))
        loop.close()
        self.assertEqual(("Tank", None), result)

    def test_check_valid_reaction_dps(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("DPS"))
        loop.close()
        self.assertEqual(("Dps", None), result)

    def test_check_valid_reaction_healer(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Healer"))
        loop.close()
        self.assertEqual(("Healer", None), result)

    def test_check_valid_reaction_t_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇹"))
        loop.close()
        self.assertEqual(("Tank", None), result)

    def test_check_valid_reaction_d_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇩"))
        loop.close()
        self.assertEqual(("Dps", None), result)

    def test_check_valid_reaction_h_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇭"))
        loop.close()
        self.assertEqual(("Healer", None), result)

    def test_check_valid_reaction_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Thumbs_up"))
        loop.close()
        self.assertEqual(None, result)

    def test_check_valid_reaction_dual_role_Tank_Dps(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("TankDPS"))
        loop.close()
        self.assertEqual(("Dps", "Tank"), result)

    def test_check_valid_reaction_dual_role_Tank_Heal(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("TankHeal"))
        loop.close()
        self.assertEqual(("Healer", "Tank"), result)

    def test_check_valid_reaction_dual_role_Dps_Healer(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("DPSHealer"))
        loop.close()
        self.assertEqual(("Healer", "Dps"), result)

    def test_check_valid_reaction_dual_role_Tank_Dps_Healer(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("TankDPSHealer"))
        loop.close()
        self.assertEqual(("Any", None), result)