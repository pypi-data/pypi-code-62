from SimpleLanguage.code_exceptions import LanguageNotFoundException
from SimpleLanguage.code_helper import LoadDatabaseList, foundDatabasesList


class SimpleLanguage:
    def __init__(self, defaultLanguage: str = "eng", actualLanguage: str = "eng", databasePath: str = ".\\language\\"):
        """
        Init the object, assign defaultLanguage, actualLanguage, databasePath and load in memory all languages databases

        :param defaultLanguage: Use this language if strings you are search for doesn't exists in actualLanguage, default: eng
        :param actualLanguage: Use this language when you search for a string, default: eng
        :param databasePath: Path of languages databases, default: ".\\language\\"
        """

        self.actualLanguage = actualLanguage
        self.databasePath = databasePath
        self.defaultLanguage = defaultLanguage

        self.strings = LoadDatabaseList(foundDatabasesList(self.databasePath))

    def changeLanguage(self, newLanguage: str):
        """
        Change language

        :param newLanguage: Use this language when you search for a string, can not be blank
        """

        self.actualLanguage = newLanguage
        
    def changeDefaultLanguage(self, newDefaultLanguage: str):
        """
        Change default language

        :param newDefaultLanguage: Use this language if strings you are search for doesn't exists in actualLanguage, can not be blank
        """

        self.defaultLanguage = newDefaultLanguage

    def changeDatabase(self, newDatabase: str):
        """
        Change path of languages databases and reload them in memory

        :param newDatabase: Path of languages databases, can not be blank
        """

        self.databasePath = newDatabase
        self.reloadDatabases()
        # TODO: TEST

    def reloadDatabases(self):
        """
        Reload databases in memory
        """
        self.strings = LoadDatabaseList(foundDatabasesList(self.databasePath))
        # TODO: TEST, how?

    def rString(self, key: str, language: str = None) -> str:
        """
        Returns a string in the language you want

        :param key: Return the string witch match with this key
        :param language: Return string in this language, default: None, you can leave blank. If this value is None function use actualLanguage or defaultLanguage
        :rtype: str
        :return: A string
        """
        try:
            if language is not None:
                return self.strings[language][key]
            else:
                return self.strings[self.actualLanguage][key]

        except KeyError:
            try:
                return self.strings[self.defaultLanguage][key]
            except KeyError:
                raise LanguageNotFoundException("This language or this strings is not in our database")
