class Verdict:
    def __init__(self, short_name, name, return_code):
        self.short_name = short_name
        self.name = name
        self.return_code = return_code
    def to_string(self):
        return self.short_name + ': ' + self.name

Correct = Verdict('AC', 'All Correct', 0)
# 1 and 2 reserved
WrongAnswer = Verdict('WA', 'Wrong Answer', 3)
PresentationError = Verdict('PE', 'Presentation Error', 4)

class Response:
    def __init__(self, verdict, message=''):
        self.verdict = verdict
        self.message = message
    def to_string(self):
        ret = self.verdict.to_string()
        if self.message != '':
            ret = ret + '\n' + self.message
        return ret
    def to_JSON(self):
        return {
            self.verdict,
            self.message
        }
