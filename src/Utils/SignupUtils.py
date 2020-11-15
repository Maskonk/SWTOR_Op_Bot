async def check_duplicate(op: dict, user_nick: str) -> bool:
    """
    Checks if the user is already signed up to the given operation.
    :param op: The operation details dictionary.
    :param user_nick: The users nickname
    :return: Booleon True if the user is already signed up to the operation.
    """
    sign_ups = op["Sign-ups"]["Tank"] + op["Sign-ups"]["Dps"] + op["Sign-ups"]["Healer"]
    for sign in sign_ups:
        if user_nick in sign:
            return True
    for i, user in enumerate(op["Sign-ups"]["Reserve"]):
        if user_nick in user:
            return True
    return False


async def check_role_change(op: dict, user_nick: str, main_role: str, alt_role: str) -> bool:
    """
    Checks if the user has changed their role.
    :param op: The operation details dictionary.
    :param user_nick: The users nickname
    :param main_role: The new main role of the user.
    :param alt_role: The optional alternative role of the user.
    :return: Booleon True if the user has changed one of both of the roles they are signing up as.
    """
    alt_change = False
    main_change = False

    if main_role == "Any":
        roles = ["Dps", "Tank", "Healer"]

        for role in roles:
            found = False
            for user in op["Sign-ups"][role]:
                if user_nick + " (Any)" in user:
                    found = True
                    break
            if found:
                return False
        else:
            return True

    else:
        for user in op["Sign-ups"][main_role]:
            if user_nick in user:
                break
        else:
            main_change = True

    if alt_role and alt_role != "Any":
        if user_nick not in op["Sign-ups"][f"Alternate_{alt_role}"]:
            alt_change = True
    elif not alt_role:
        roles = ["Tank", "Dps", "Healer"]
        for role in roles:
            if user_nick in op["Sign-ups"][f"Alternate_{role}"]:
                alt_change = True
    return main_change or alt_change
