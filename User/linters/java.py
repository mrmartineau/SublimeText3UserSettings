from lint import Linter

class Java(Linter):
    language = 'java'
    cmd = ('javac', '-Xlint')
    regex = r'^[^:]+:(?P<line>\d+): (?P<error>.*)$'

    # this linter doesn't work very well with projects/imports
    defaults = {
        'disable': True,
    }

    def run(self, *args):
        return self.tmpfile(*args, suffix='.java')
