def sanity_check(sql_fields):
    """ Will sanity check the fields
        return true, if we can run it"""

    if (type(sql_fields) in [int, bool]) or sql_fields.replace(" ", "").isalnum():
        return True
    else:
        raise ValueError(f"{sql_fields} isn't an accepted field value.")


def to_str(my_str, password_hash=False):
    """ Will return the string surrounded by
        double quotes, useful for SQL query
        Or if it's a bool return TRUE/FALSE
        Or if it's a number the number as it is
        Or if it's a list will call back this function
        and return all the field separated by ',' """

    if password_hash:
        return "\"" + my_str + "\""

    if type(my_str) is list:
        return ",".join([to_str(i) for i in my_str])

    if sanity_check(my_str):
        if type(my_str) is str:
            return "\"" + my_str + "\""
        elif type(my_str) is int:
            return str(my_str)
        # For better looking sql queries
        elif my_str is True:
            return 1
        elif my_str is False:
            return 0

    raise TypeError(f"{type(my_str)} type isn't accepted.")