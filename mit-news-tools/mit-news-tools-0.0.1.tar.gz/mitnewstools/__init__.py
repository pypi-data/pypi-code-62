from confusables import normalize


def asciify(text: str, return_failed_chars=False):
    """
    Takes a string and returns an ASCII version of it.
    If there is no suitable ASCII version of the string, it will be replaced by a space.

    If return_failed_chars is True, it returns a tuple.
    The first element is the asciified string.
    The second element is a list of characters that failed to be converted into ASCII and instead were converted to spaces.
    example: "asciified string", [":)", ":—)"]

    :param text: A string that you want to make sure is ASCII.
    :param return_failed_chars: If true, will return a list of characters that have failed to convert to ASCII
    :return: an ASCII version of the input string;
            if return_failed_chars is True, it also returns a list of characters that failed to be converted into ASCII
            and instead were converted to spaces
    """
    retstr = ""

    numconvchar = 0
    failedchars = []

    for char in text:
        if not char.isascii():
            newchar = normalize(char, prioritize_alpha=True)[0]

            # attempts to make newchar ascii
            if not newchar.isascii():
                if newchar == '—':
                    newchar = '--'
                    # print("YAY: " + char + " -> "+ newchar)
                else:
                    for posschar in normalize(char):
                        # print(char)
                        if posschar.isascii():
                            newchar = posschar
                            # print("YAY: " + char + " -> "+ newchar)
                            break

            if not newchar.isascii():
                # print("RIP this char cannot be processed: " + char + " -> "+ newchar)

                # print(char.encode('raw_unicode_escape'))
                # print(newchar.encode('raw_unicode_escape'))

                newchar = " "

                failedchars.append(char)

            else:
                numconvchar += 1
            # elif newchar not in ["'", '"', "...", '-']:
            # print("YAY: " + char + " -> "+ newchar)
            retstr += newchar
        else:
            retstr += char

    # print(str(numconvchar) + ' characters conversted to ASCII | ' + str(numfailedchar) + " failed")

    if return_failed_chars:
        return retstr, failedchars
    return retstr
