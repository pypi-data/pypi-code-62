import time

numbers = ("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
           "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")

clockface = ("o'clock", "quarter", "half", "quarter")


def talk(time_input):
    """
    Converts a time string to the equivalent english language sentence
    :param time_input: The time string to convert
    :return: The english language equivalent of the provided time string
    """
    hour, minute, context = get_context(time_input)
    words = convert_to_words(hour, minute, context)
    return " ".join(filter(None, words)).strip().capitalize()


def get_context(time_input):
    """
    Determine if we want to talk in the context of the current hour or the next hour
    Sets the time values relevant to the context
    :param time_input: The time string from which to base context
    :return: a tuple containing the contextualised hour and minute,
    """
    try:
        formatted_time = time.strptime(time_input, "%H:%M")
        separator = ":"
    except ValueError:
        try:
            formatted_time = time.strptime(time_input, "%H.%M")
            separator = "."
        except ValueError:
            formatted_time = time.strptime(time_input, "%H%M")
            separator = ""

    twelve_hour_time = time.strftime("%I{}%M".format(separator), formatted_time)

    if separator:
        hour, minute = map(int, twelve_hour_time.split(separator))
    else:
        hour = int(twelve_hour_time[:2])
        minute = int(twelve_hour_time[-2:])

    context = "past"
    if minute > 30:
        if hour == 12:
            hour = 0
        minute = 60 - minute
        context = "to"
        hour += 1
    return hour, minute, context


def convert_to_words(hour, minute, context):
    """
    Convert the given hour and minute into words,
    :param hour: int representing the hour
    :param minute: int representing the minute
    :param context: The context of how the current time is expressed, must be 'to' or 'past'
    :return: a list of the words giving a meaningful english language representation of the time
    """
    if minute == 0:
        # if it's zero then we are on the hour
        return [numbers[hour], clockface[minute]]

    # check if the minute hand would be on one of the quarter increments i.e. o'clock, quarter, half
    if (minute % 15) == 0:
        return [clockface[int(minute / 15)], context, numbers[hour]]

    # if we arent at a quarter increment then just convert the numbers to words
    tens = (minute // 10) * 10
    ones = minute % 10
    words = []
    if tens == 10:
        # if it's a teen then just get the word
        words.append(numbers[minute])
    else:
        # if it's not a teen then we need separate words for the tens and ones
        words.extend([numbers[tens], numbers[ones]])

    # commonly times are expressed without the word 'minutes' when its a multiple of 5
    # if it's not a multiple of 5 we normally add 'minutes', since saying '18 past 12' for example, sounds odd
    if ones % 5 != 0:
        words.append("minutes")

    words.extend([context, numbers[hour]])
    return words
