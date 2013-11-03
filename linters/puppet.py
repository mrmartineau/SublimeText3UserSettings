from lint import Linter

class Puppet(Linter):
    language = 'puppet'
    cmd = ('puppet', 'parser', 'validate', '--color=false')
    regex = r'^([^:]+:){2}\s*(?P<error>(Syntax error at|Could not match) \'?(?P<near>[^ ]*?)\'?.*) at [^:]*:(?P<line>\d+)$'

    def run(self, cmd, code):
        return self.tmpfile(cmd, code, suffix='.puppet')
