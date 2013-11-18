from lint import Linter
import os

class Nasm(Linter):
    language = 'x86 assembly'
    cmd = ('nasm', '-X', 'gnu', '-I.', '-o', os.devnull)
    regex = r'^[^:]+:(?P<line>\d+): (?P<error>.*)$'

    def run(self, cmd, code):
        return self.tmpfile(cmd, code, suffix='.asm')
