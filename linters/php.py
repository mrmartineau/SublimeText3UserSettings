from lint import Linter

class PHP(Linter):
    language = ('php', 'html')
    cmd = ('php', '-l', '-n', '-d display_errors=On')
    regex = r'^Parse error:\s*(?P<type>parse|syntax) error,?\s*(?P<error>.+?)?\s+in\s+.+?\s*line\s+(?P<line>\d+)'

    def match_error(self, r, line):
        match, row, col, error, near = super().match_error(r, line)

        if match and match.group('type') == 'parse' and not error:
            error = 'parse error'

        return match, row, col, error, near
