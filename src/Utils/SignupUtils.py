class SignupUtils:
    @staticmethod
    async def check_duplicate(op: dict, user_nick: str) -> bool:
        """
        Checks if the user is already signed up to the given operation.
        :param op: The operation details dictionary.
        :param user_nick: The users nickname
        :return: Booleon True if the user is already signed up to the operation.
        """
        # sign_ups = op["Sign-ups"]["Tank"] + op["Sign-ups"]["Dps"] + op["Sign-ups"]["Healer"]
        for sign in op["Sign-ups"]["Roster"]:
            if user_nick in sign.get("name", None):
                return True
        for user in op["Sign-ups"]["Reserves"]:
            if user_nick in user.get("name", None):
                return True
        return False

    @staticmethod
    async def check_role_change(op: dict, user_nick: str, main_role: str, alt_role: str) -> bool:
        """
        Checks if the user has changed their role.
        :param op: The operation details dictionary.
        :param user_nick: The users nickname
        :param main_role: The new main role of the user.
        :param alt_role: The optional alternative role of the user.
        :return: Booleon True if the user has changed one of both of the roles they are signing up as.
        """

        for sign in op["Sign-ups"]["Roster"]:
            if sign.get("name", None) == user_nick:
                return sign.get("main-role", None) != main_role or sign.get("alt-role", None) != alt_role
        return True
