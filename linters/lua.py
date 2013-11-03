from lint import Linter

class Lua(Linter):
    language = 'lua'
    cmd = ('luac', '-p')
    regex = '^luac: [^:]+:(?P<line>\d+): (?P<error>.+?)(?P<near> near .+)?'

    def run(self, cmd, code):
        return self.tmpfile(cmd, code, suffix='.lua')
