from unittest import TestCase
import asyncio
from ..Utils.ReactionUtils import check_valid_reaction


class Test(TestCase):
    def test_check_valid_reaction_tank(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Tank"))
        loop.close()
        self.assertEqual("Tank", result)

    def test_check_valid_reaction_dps(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("DPS"))
        loop.close()
        self.assertEqual("Dps", result)

    def test_check_valid_reaction_healer(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Healer"))
        loop.close()
        self.assertEqual("Healer", result)

    def test_check_valid_reaction_t_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇹"))
        loop.close()
        self.assertEqual("Tank", result)

    def test_check_valid_reaction_d_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇩"))
        loop.close()
        self.assertEqual("Dps", result)

    def test_check_valid_reaction_h_indicator(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("🇭"))
        loop.close()
        self.assertEqual("Healer", result)

    def test_check_valid_reaction_invalid(self):
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(check_valid_reaction("Thumbs_up"))
        loop.close()
        self.assertEqual(None, result)