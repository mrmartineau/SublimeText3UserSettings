from lint import Linter

class XML(Linter):
    language = 'xml'
    cmd = ('xmllint', '-noout', '-')
    regex = r'^.+:(?P<line>\d+):\s+(parser error : )?(?P<error>.+)'
