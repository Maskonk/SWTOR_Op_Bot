from dateutil.parser import parse
from datetime import datetime


async def validate_time_input(date: str, time: str) -> bool:
    """
    Checks the users input to ensure the date and time inputs are valid and not yet passed.
    :param date: The Date input by the user.
    :param time: The Time input by the user.
    :return: Booleon True if the date and time inputs are valid.
    """
    dt = parse(f"{date} {time}", dayfirst=True)
    if dt < datetime.today():
        return False
    else:
        return True


async def validate_difficulty_input(difficulty: str) -> bool:
    """
    Checks the users input to ensure the difficulty input is valid.
    :param difficulty: The difficulty input by the user.
    :return: Booleon True if the difficulty input is valid.
    """
    return difficulty.lower() in ["sm", "hm", "nim", "na", "vm", "mm"]


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