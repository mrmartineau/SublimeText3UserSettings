from lint import Linter

class Ruby(Linter):
    language = 'ruby'
    cmd = ('ruby', '-wc')
    regex = r'^.+:(?P<line>\d+):\s+(?P<error>.+)'
