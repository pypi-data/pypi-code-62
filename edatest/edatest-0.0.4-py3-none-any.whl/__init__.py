class Edatest:
    def __init__(self):
        self.PINK = '\033[95m'
        self.BLUE = '\033[94m'
        self.GOOD = '\033[92m'
        self.WARN = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'

    def assert_equals(self, answer, correct, hint=False):
        if answer == correct:
            print(self.GOOD + self.BOLD + "✓ TEST PASSED" + self.ENDC)
        else:
            print(self.FAIL + self.BOLD + "⨉ FAILED" + self.ENDC + ": \"" + self.response(answer) + "\" should equal \"" + self.response(correct) + "\"")

            if hint and type(hint) == str:
                print(self.FAIL + ">>" + self.BLUE +" 🛈 HINT: " + self.ENDC + "\"" + hint + "\"")

    def response(self, response):
        return str(response)