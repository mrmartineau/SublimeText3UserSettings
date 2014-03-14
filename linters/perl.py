from lint import Linter

class Perl(Linter):
    language = 'perl'
    cmd = ('perl', '-c')
    regex = r'(?P<error>.+?) at .+? line (?P<line>\d+)(, near "(?P<near>.+?)")?'
