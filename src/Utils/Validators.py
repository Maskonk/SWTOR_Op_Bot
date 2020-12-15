from dateutil.parser import parse
from datetime import datetime
from dateutil.parser._parser import ParserError


class Validators():
    @staticmethod
    async def validate_time_input(date: str, time: str) -> bool:
        """
        Checks the users input to ensure the date and time inputs are valid and not yet passed.
        :param date: The Date input by the user.
        :param time: The Time input by the user.
        :return: Booleon True if the date and time inputs are valid.
        """
        try:
            dt = parse(f"{date} {time}", dayfirst=True)
        except ParserError:
            return False

        if dt < datetime.today():
            return False
        else:
            return True

    @staticmethod
    async def validate_difficulty_input(difficulty: str) -> bool:
        """
        Checks the users input to ensure the difficulty input is valid.
        :param difficulty: The difficulty input by the user.
        :return: Booleon True if the difficulty input is valid.
        """
        return difficulty.lower() in ["sm", "hm", "nim", "na", "vm", "mm"]

    @staticmethod
    async def validate_role(role: str) -> str:
        """
        Checks the role given is valid and converts any short hand role to the proper name.
        :param role: The role of the user.
        :return: The long version of the users role.
        """
        if role.lower() in ["t", "tank", "d", "dps", "h", "heals", "healer", "heal", "a", "any", "r", "reserve"]:
            if role[0].lower() == "t":
                return "Tank"
            elif role[0].lower() == "d":
                return "Dps"
            elif role[0].lower() == "h":
                return "Healer"
            elif role[0].lower() == "a":
                return "Any"
            elif role[0].lower() == "r":
                return "Reserve"
        else:
            return ""

    @staticmethod
    async def validate_side_input(side: str) -> str:
        """
        Checks the side given is valid and converts names to a standard.
        :param side: The side the operation is to take place
        :return: The standard name of the side or None if invalid.
        """
        if side.lower() in ["imp", "imps", "imperial", "i"]:
            return "Imp"
        elif side.lower() in ["rep", "reps", "republic", "pub", "r"]:
            return "Rep"
        else:
            return None

    @staticmethod
    async def validate_size_input(size: str, sizes: dict) -> bool:
        """
        Checks the users input to ensure the size input is valid.
        :param size: The size input by the user.
        :param sizes: Dictionary of valid sizes to check against.
        :return: Booleon True if the size input is valid.
        """
        return str(size) in sizes.keys()

    @staticmethod
    async def validate_operation_input(op: str, operations: dict) -> bool:
        """
        Checks the users input to ensure the operation input is valid.
        :param op: The Operation input by the user.
        :param operations: Dictionary of valid operations to check against.
        :return: Booleon True if the operation input is valid.
        """
        return op.lower() in operations.keys() or op.lower() == "random"

    @staticmethod
    async def validate_operation_channel(input_channel_id: int, server_config: dict) -> bool:
        """
        Validator for operation commands channel input. Checks if the input channel is a valid channel for operation
        commands.
        :param input_channel_id: The inputs channel id.
        :param server_config: Dictionary of the configuration for the server.
        :return: Boolean True if channel is valid.
        """
        config_id_list = server_config.get("Operation_channels", [])
        if not config_id_list:
            return True
        return input_channel_id in config_id_list

    @staticmethod
    async def validate_sign_up_channel(input_channel_id: int, server_config: dict) -> bool:
        """
        Validator for operation sign up commands channel input. Checks if the input channel is a valid channel for operation
        sign up commands.
        :param input_channel_id: The inputs channel id.
        :param server_config: Dictionary of the configuration for the server.
        :return: Boolean True if channel is valid.
        """
        config_id_list = server_config.get("Signup_channels", [])
        if not config_id_list:
            return True
        return input_channel_id in config_id_list

    @staticmethod
    async def validate_swtor_channel(input_channel_id: int, server_config: dict) -> bool:
        """
        Validator for swtor commands channel input. Checks if the input channel is a valid channel for general swtor
        commands.
        :param input_channel_id: The inputs channel id.
        :param server_config: Dictionary of the configuration for the server.
        :return: Boolean True if channel is valid.
        """
        config_id_list = server_config.get("Fun_channels", [])
        if not config_id_list:
            return True
        return input_channel_id in config_id_list
