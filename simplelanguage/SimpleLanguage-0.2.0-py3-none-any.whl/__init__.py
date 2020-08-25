from SimpleLanguage.code_main import SimpleLanguage


def init(defaultLanguage: str = "eng", actualLanguage: str = "eng", databasePath: str = ".\\language\\"):
    """
    Init the object, assign defaultLanguage, actualLanguage, databasePath and load in memory all languages databases

    :param defaultLanguage: Use this language if strings you are search for doesn't exists in actualLanguage, default: eng
    :param actualLanguage: Use this language when you search for a string, default: eng
    :param databasePath: Path of languages databases, default: ".\\language\\"
    """

    return SimpleLanguage(defaultLanguage, actualLanguage, databasePath)