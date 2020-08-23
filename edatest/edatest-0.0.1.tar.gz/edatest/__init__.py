class Edatest:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def assert_equals(self, answer, correct, *optional):
        if answer == correct:
            print(self.OKGREEN + self.BOLD + "✓ CORRECT ANSWER" + self.ENDC)
        else:
            print(self.FAIL + self.BOLD + "❌ FAILED" + self.ENDC + ": \"" + self.response(answer) + "\" should equal \"" + self.response(correct) + "\"")

    def response(self, response):
        if response == True:
            return "True"
        elif response == False:
            return "False"
        else:
            return response