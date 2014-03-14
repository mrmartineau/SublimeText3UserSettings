from lint import Linter

class HTML(Linter):
    language = 'html'
    cmd = ('tidy', '-q', '-e', '-utf8')
    regex = r'^line (?P<line>\d+) column (?P<col>\d+) - (Warning|Error)?\s*:?\s*(?P<error>.+)$'
