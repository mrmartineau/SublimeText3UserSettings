from lint import Linter

class HAML(Linter):
    language = 'ruby haml'
    cmd = ('haml', '-c')
    regex = r'^.*line (?P<line>\d+):\s*(?P<error>.+)$'
