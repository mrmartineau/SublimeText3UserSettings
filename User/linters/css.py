from lint import Linter

class CSS(Linter):
    language = 'css'
    cmd = ('csslint',)
    regex = (
        r'^\d+: (?P<type>(error|warning)) at line (?P<line>\d+), col (?P<col>\d+)$\W'
        r'^(?P<error>.*)$'
    )
    multiline = True

    def run(self, cmd, code):
        return self.tmpfile(cmd, code, suffix='.css')
