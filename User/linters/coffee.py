from lint import Linter

class Coffee(Linter):
    language = 'coffeescript'
    cmd = ('coffee', '--compile', '--stdio')
    regex = r'^[A-Za-z]+: (?P<error>.+) on line (?P<line>\d+)'
