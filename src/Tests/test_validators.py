from unittest import TestCase
from ..Utils.Validators import Validators
from datetime import datetime


class TestValidators(TestCase):
    def setUp(self) -> None:
        pass

    def test_validate_time_input_valid(self):
        assert(Validators.validate_time_input("11/12/2021", "11:20"), True)

    def test_validate_time_input_invalid(self):
        assert(Validators.validate_time_input("11/12/19", "11:20"), True)

    def test_validate_difficulty_input(self):
        self.fail()

    def test_validate_role(self):
        self.fail()

    def test_validate_side_input(self):
        self.fail()

    def test_validate_size_input(self):
        self.fail()

    def test_validate_operation_input(self):
        self.fail()

    def test_validate_operation_channel(self):
        self.fail()

    def test_validate_sign_up_channel(self):
        self.fail()

    def test_validate_swtor_channel(self):
        self.fail()
