"""
Splunk specific boolean evaluation method
"""


def normalizeBoolean(input_param, enableStrictMode=False, includeIntegers=True):
    """
    Tries to convert a value to Boolean.  Accepts the following pairs:
    true/false t/f/ 0/1 yes/no on/off y/n

    If given a dictionary, this function will attempt to iterate over the dictionary
    and normalize each item.

    If enableStrictMode is True, then a ValueError will be raised if the input
    value is not a recognized boolean.

    If enableStrictMode is False (default), then the input will be returned
    unchanged if it is not recognized as a boolean.  Thus, they will have the
    truth value of the python language.

    NOTE: Use this method judiciously, as you may be casting integer values
    into boolean when you don't want to.  If you do want to get integer values,
    the idiom for that is:

        try:
            v = int(v)
        except ValueError:
            v = splunk.util.normalizeBoolean(v)

    This casts integer-like values into 'int', and others into boolean.
    """

    trueThings = ["true", "t", "on", "yes", "y", "ff"]
    falseThings = ["false", "f", "off", "no", "n"]

    if includeIntegers:
        trueThings.append("1")
        falseThings.append("0")

    def norm(input_param):
        if input_param is True:
            return True
        if input_param is False:
            return False

        try:
            test = input_param.strip().lower()
        except:
            return input_param

        if test in trueThings:
            return True
        if test in falseThings:
            return False
        if enableStrictMode:
            raise ValueError("Unable to cast value to boolean: {}".format(input))
        return input_param

    if isinstance(input_param, dict):
        for k, v in input_param.items():
            input_param[k] = norm(v)
        return input_param

    return norm(input_param)
